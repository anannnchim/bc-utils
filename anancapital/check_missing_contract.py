#!/usr/bin/env python3
"""
check_missing_contract.py

Interactive contract coverage checker.

Features:
- Repeated instrument checking
- Press Enter to exit
- Case-insensitive matching
- Smart dominant-gap detection
- Dynamic project root detection
- Read-only safe
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Tuple
import re


# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

PREFIXES = ("Day", "Hour")

CONTRACT_PATTERN = re.compile(
    r"^(Day|Hour)_(?P<inst>[A-Za-z0-9_\-]+)_(?P<yyyymm>\d{6})00\.csv$"
)


# --------------------------------------------------
# Utilities
# --------------------------------------------------

def ask(prompt: str) -> str | None:
    value = input(prompt).strip()
    return value if value else None


def parse_contract_filename(filename: str) -> Tuple[str, str, int] | None:
    m = CONTRACT_PATTERN.match(filename)
    if not m:
        return None

    return (
        m.group(1),
        m.group("inst"),
        int(m.group("yyyymm")),
    )


def yyyymm_to_abs_month(yyyymm: int) -> int:
    year = yyyymm // 100
    month = yyyymm % 100
    return year * 12 + month


def abs_month_to_yyyymm(abs_month: int) -> int:
    year = abs_month // 12
    month = abs_month % 12
    if month == 0:
        year -= 1
        month = 12
    return year * 100 + month


def detect_missing_contracts(
    sorted_contracts: List[int],
) -> Tuple[List[int], int, Dict[int, int]]:

    if len(sorted_contracts) < 2:
        return [], 0, {}

    abs_months = [yyyymm_to_abs_month(x) for x in sorted_contracts]

    gaps = [
        abs_months[i + 1] - abs_months[i]
        for i in range(len(abs_months) - 1)
    ]

    gap_counts: Dict[int, int] = {}
    for g in gaps:
        gap_counts[g] = gap_counts.get(g, 0) + 1

    expected_gap = max(gap_counts, key=gap_counts.get)

    missing: List[int] = []

    for i in range(len(abs_months) - 1):
        current = abs_months[i]
        nxt = abs_months[i + 1]
        gap = nxt - current

        if gap > expected_gap:
            m = current + expected_gap
            while m < nxt:
                missing.append(abs_month_to_yyyymm(m))
                m += expected_gap

    return missing, expected_gap, gap_counts


def collect_contracts(
    instrument_input: str,
) -> Tuple[Dict[str, List[int]], str | None]:

    result: Dict[str, List[int]] = {p: [] for p in PREFIXES}
    actual_name: str | None = None

    for p in DATA_DIR.iterdir():
        if not p.is_file() or p.suffix.lower() != ".csv":
            continue

        parsed = parse_contract_filename(p.name)
        if not parsed:
            continue

        freq, inst, yyyymm = parsed

        if inst.lower() == instrument_input.lower():
            actual_name = inst
            result[freq].append(yyyymm)

    for freq in result:
        result[freq] = sorted(result[freq])

    return result, actual_name


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

def run_check(instrument_input: str) -> None:

    contracts, actual_name = collect_contracts(instrument_input)

    if not actual_name:
        print(f"\nInstrument '{instrument_input}' not found.\n")
        return

    print(f"\nInstrument : {actual_name}\n")

    for freq in PREFIXES:
        series = contracts.get(freq, [])

        print(f"--- {freq} Series ---")

        if not series:
            print("No contracts found.\n")
            continue

        start = series[0]
        end = series[-1]

        missing, expected_gap, gap_distribution = detect_missing_contracts(series)

        print(f"Contracts found : {len(series)}")
        print(f"Start contract  : {start}")
        print(f"End contract    : {end}")
        print(f"Detected gap    : {expected_gap} month(s)")

        print("Gap distribution:")
        for gap, count in sorted(gap_distribution.items()):
            print(f"  {gap} month(s) : {count}")

        print(f"Missing count   : {len(missing)}")

        if missing:
            print("Missing contracts:")
            for m in missing:
                print(f"  {m}")

        print()


def main() -> int:
    if not DATA_DIR.exists():
        print(f"Data directory not found: {DATA_DIR}")
        return 1

    print("=== Interactive Missing Contract Checker ===")
    print("Press Enter without typing anything to exit.\n")

    while True:
        instrument_input = ask("Enter instrument code: ")

        if not instrument_input:
            print("\nExiting.")
            break

        run_check(instrument_input)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
