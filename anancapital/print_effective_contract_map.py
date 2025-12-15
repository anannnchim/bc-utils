#!/usr/bin/env python3
"""
Print the effective (final) CONTRACT_MAP and EXCHANGES after applying
private overrides/removals (if present).

Run from repo root:
  python anancapital/print_effective_contract_map.py

Or from anywhere:
  python /Users/nanthawat/PycharmProjects/bc-utils/anancapital/print_effective_contract_map.py
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict


def _repo_root_from_this_file() -> str:
    # anancapital/print_effective_contract_map.py -> repo root is one level up
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _import_effective_maps() -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Import bcutils.config which already applies:
      - CONTRACT_MAP_REMOVALS
      - CONTRACT_MAP_OVERRIDES
      - EXCHANGES_REMOVALS
      - EXCHANGES_OVERRIDES
    via your try/except ImportError block.

    Returns the final dictionaries.
    """
    try:
        from bcutils.config import CONTRACT_MAP, EXCHANGES  # type: ignore
    except ModuleNotFoundError:
        # Ensure repo root is on sys.path
        repo_root = _repo_root_from_this_file()
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        from bcutils.config import CONTRACT_MAP, EXCHANGES  # type: ignore

    return CONTRACT_MAP, EXCHANGES


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


def main() -> None:
    contract_map, exchanges = _import_effective_maps()

    print("\n=== Effective CONTRACT_MAP (after private overrides/removals if any) ===")
    print(f"Total contracts: {len(contract_map)}")
    print(_safe_json(contract_map))

    print("\n=== Effective EXCHANGES (after private overrides/removals if any) ===")
    print(f"Total exchanges: {len(exchanges)}")
    print(_safe_json(exchanges))


if __name__ == "__main__":
    main()
