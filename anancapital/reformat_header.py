#!/usr/bin/env python3
"""
reformat_header.py

Goal:
- For a given instrument code, find all files in /Users/nanthawat/PycharmProjects/bc-utils/data
  named like:
    Day_<INSTRUMENT>_*.csv
    Hour_<INSTRUMENT>_*.csv
- If the CSV header has column "Latest", rename it to "Close"
- Do NOT change anything else in the file.
"""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path
from typing import List


DATA_DIR = Path("/Users/nanthawat/PycharmProjects/bc-utils/data")
PREFIXES = ("Day_", "Hour_")


def find_files_for_instrument(instrument: str, data_dir: Path) -> List[Path]:
    instrument = instrument.strip()
    matches: List[Path] = []

    for p in data_dir.iterdir():
        if not (p.is_file() and p.suffix.lower() == ".csv"):
            continue

        # Match either Day_<instrument>_*.csv or Hour_<instrument>_*.csv
        for pref in PREFIXES:
            if p.name.startswith(f"{pref}{instrument}_"):
                matches.append(p)
                break

    return sorted(matches)


def rewrite_header_latest_to_close(csv_path: Path) -> bool:
    """
    Returns True if file was modified, False if no change needed.
    """
    # Quick check: read first line only
    encodings_to_try = ["utf-8", "latin-1"]
    first_line = None
    used_encoding = None

    for enc in encodings_to_try:
        try:
            with csv_path.open("r", newline="", encoding=enc) as f:
                first_line = f.readline()
            used_encoding = enc
            break
        except UnicodeDecodeError:
            continue

    if not first_line:
        return False

    header = [h.strip() for h in first_line.strip("\r\n").split(",")]
    if "Latest" not in header:
        return False

    new_header = ["Close" if h == "Latest" else h for h in header]

    # Rewrite whole file safely (atomic replace)
    last_err = None
    for enc in ([used_encoding] if used_encoding else []) + [e for e in encodings_to_try if e != used_encoding]:
        try:
            with csv_path.open("r", newline="", encoding=enc) as rf:
                reader = csv.reader(rf)
                rows = list(reader)

            if not rows:
                return False

            rows[0] = new_header

            tmp_fd, tmp_name = tempfile.mkstemp(
                prefix=csv_path.stem + "_", suffix=".tmp", dir=str(csv_path.parent)
            )
            os.close(tmp_fd)
            tmp_path = Path(tmp_name)

            try:
                with tmp_path.open("w", newline="", encoding=enc) as wf:
                    writer = csv.writer(wf)
                    writer.writerows(rows)

                tmp_path.replace(csv_path)
            finally:
                if tmp_path.exists():
                    try:
                        tmp_path.unlink()
                    except OSError:
                        pass

            return True

        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"Failed to process {csv_path} due to: {last_err}")


def main() -> int:
    instrument = input("Instrument code (e.g., BUND): ").strip()
    if not instrument:
        print("No instrument code provided. Exiting.")
        return 1

    if not DATA_DIR.exists():
        print(f"Data directory not found: {DATA_DIR}")
        return 1

    files = find_files_for_instrument(instrument, DATA_DIR)
    if not files:
        print(f"No Day_/Hour_ files found for instrument '{instrument}' in {DATA_DIR}")
        return 0

    modified = 0
    skipped = 0
    failed = 0

    for p in files:
        try:
            changed = rewrite_header_latest_to_close(p)
            if changed:
                modified += 1
                print(f"[MODIFIED] {p.name} (Latest -> Close)")
            else:
                skipped += 1
                print(f"[SKIPPED ] {p.name} (no 'Latest' column)")
        except Exception as e:
            failed += 1
            print(f"[FAILED  ] {p.name}: {e}")

    print("\n=== Summary ===")
    print(f"Instrument : {instrument}")
    print(f"Directory  : {DATA_DIR}")
    print(f"Files found: {len(files)}")
    print(f"Modified   : {modified}")
    print(f"Skipped    : {skipped}")
    print(f"Failed     : {failed}")

    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
