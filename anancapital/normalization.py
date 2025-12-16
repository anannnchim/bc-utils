# bcutils/normalization/barchart_prices.py
from __future__ import annotations

import pandas as pd

class BarchartPriceNormalizer:
    """
    Converts Barchart-shaped dataframes into our internal canonical schema.
    Canonical: index=Time (tz-aware UTC), columns: Open, High, Low, Close, Volume
    """

    # alias map: support multiple possible vendor names
    COLUMN_ALIASES = {
        "Close": ["Close", "Last", "Latest", "Settlement", "Settle"],
        "Open": ["Open", "Open Price", "openPrice"],
        "High": ["High", "High Price", "highPrice"],
        "Low":  ["Low", "Low Price", "lowPrice"],
        "Volume": ["Volume", "volume"],
        "Time": ["Time", "tradeTime", "Date"],
    }

    REQUIRED = ["Open", "High", "Low", "Close", "Volume"]

    @classmethod
    def normalize(cls, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame([])

        df = df.copy()

        # 1) Rename columns using aliases (Latest -> Close, etc.)
        rename_map = {}
        for canonical, aliases in cls.COLUMN_ALIASES.items():
            for a in aliases:
                if a in df.columns:
                    rename_map[a] = canonical
                    break
        df = df.rename(columns=rename_map)

        # 2) Ensure index is Time (already set in your code, but keep robust)
        if "Time" in df.columns:
            df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
            df = df.set_index("Time")

        # 3) Enforce required columns
        missing = [c for c in cls.REQUIRED if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns after normalization: {missing}. "
                             f"Available: {list(df.columns)}")

        # 4) Keep only canonical columns in canonical order
        df = df[cls.REQUIRED]

        return df
