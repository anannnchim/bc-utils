from __future__ import annotations

import pandas as pd


class BarchartPriceNormalizer:
    """Normalize vendor data to the canonical Barchart price schema."""

    COLUMN_ALIASES = {
        "Close": ["Close", "Last", "Latest", "Settlement", "Settle"],
        "Open": ["Open", "Open Price", "openPrice"],
        "High": ["High", "High Price", "highPrice"],
        "Low": ["Low", "Low Price", "lowPrice"],
        "Volume": ["Volume", "volume"],
        "Time": ["Time", "tradeTime", "Date"],
    }
    REQUIRED = ["Open", "High", "Low", "Close", "Volume"]

    @classmethod
    def normalize(cls, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame()

        normalized = df.copy()
        rename_map = {}
        for canonical, aliases in cls.COLUMN_ALIASES.items():
            for alias in aliases:
                if alias in normalized.columns:
                    rename_map[alias] = canonical
                    break
        normalized = normalized.rename(columns=rename_map)

        if "Time" in normalized.columns:
            normalized["Time"] = pd.to_datetime(normalized["Time"], errors="coerce")
            normalized = normalized.set_index("Time")

        missing = [column for column in cls.REQUIRED if column not in normalized]
        if missing:
            raise ValueError(
                "Missing required columns after normalization: "
                f"{missing}. Available: {list(normalized.columns)}"
            )

        return normalized[cls.REQUIRED]
