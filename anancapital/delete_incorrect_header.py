#!/usr/bin/env python3
"""
delete_incorrect_header.py

Deletes CSV files in /Users/nanthawat/PycharmProjects/bc-utils/data where the header contains "Latest"
(i.e., incorrect format: Time,Open,High,Low,Latest,Volume)

Scope:
- Both Day_* and Hour_* files
- Only .csv files
- Only deletes if the FIRST LINE (header row) contains an exact column named "Latest"

Safety:
- Shows a list + summary
- Requires a confirmation "DELETE" before removing anything
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple


# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PREFIXES = ("Day_", "Hour_")

ENCODINGS_TO_TRY = ("utf-8", "latin-1")


def read_first_line(path: Path) -> str:
    for enc in ENCODINGS_TO_TRY:
        try:
            with path.open("r", encoding=enc, newline="") as f:
                return f.readline()
        except UnicodeDecodeError:
            continue
    # If we can't decode with common encodings, treat as unreadable and skip
    raise UnicodeDecodeError("unknown", b"", 0, 1, "Unable to decode file header with utf-8/latin-1")


def header_has_latest(header_line: str) -> bool:
    if not header_line:
        return False
    cols = [c.strip() for c in header_line.strip("\r\n").split(",")]
    return "Latest" in cols


def find_candidate_files(data_dir: Path) -> List[Path]:
    files: List[Path] = []
    for p in data_dir.iterdir():
        if not (p.is_file() and p.suffix.lower() == ".csv"):
            continue
        if not any(p.name.startswith(pref) for pref in PREFIXES):
            continue
        files.append(p)
    return sorted(files)


def find_files_with_latest(data_dir: Path) -> Tuple[List[Path], List[Tuple[Path, str]]]:
    """
    Returns:
      - files_to_delete: list of files that contain "Latest" in header
      - unreadable: list of (file, error_message) that couldn't be checked
    """
    files_to_delete: List[Path] = []
    unreadable: List[Tuple[Path, str]] = []

    for p in find_candidate_files(data_dir):
        try:
            first_line = read_first_line(p)
            if header_has_latest(first_line):
                files_to_delete.append(p)
        except Exception as e:
            unreadable.append((p, str(e)))

    return files_to_delete, unreadable


def main() -> int:
    if not DATA_DIR.exists():
        print(f"Data directory not found: {DATA_DIR}")
        return 1

    files_to_delete, unreadable = find_files_with_latest(DATA_DIR)

    print(f"Directory: {DATA_DIR}")
    print(f"Scanned Day_/Hour_ CSV files: {len(find_candidate_files(DATA_DIR))}")
    print(f"Files with 'Latest' header (to delete): {len(files_to_delete)}")
    print(f"Unreadable / skipped: {len(unreadable)}")

    if unreadable:
        print("\n--- Unreadable / skipped files ---")
        for p, err in unreadable:
            print(f"[SKIP] {p.name}: {err}")

    if not files_to_delete:
        print("\nNo files found with 'Latest' in the header. Nothing to delete.")
        return 0

    print("\n--- Files that will be deleted ---")
    for p in files_to_delete:
        print(p.name)

    print("\nType DELETE to confirm deletion (anything else cancels):")
    confirm = input("> ").strip()

    if confirm != "DELETE":
        print("Cancelled. No files deleted.")
        return 0

    deleted = 0
    failed = 0

    for p in files_to_delete:
        try:
            p.unlink()
            deleted += 1
            print(f"[DELETED] {p.name}")
        except Exception as e:
            failed += 1
            print(f"[FAILED ] {p.name}: {e}")

    print("\n=== Summary ===")
    print(f"Deleted: {deleted}")
    print(f"Failed : {failed}")

    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
