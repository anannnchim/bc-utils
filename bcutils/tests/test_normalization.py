import pandas as pd
import pytest

from bcutils.normalization import BarchartPriceNormalizer


@pytest.mark.parametrize("close_column", ["Close", "Last", "Latest", "Settle"])
def test_price_normalizer_accepts_close_aliases(close_column):
    source = pd.DataFrame(
        {
            "Time": ["2025-01-02"],
            "Open": [1.0],
            "High": [2.0],
            "Low": [0.5],
            close_column: [1.5],
            "Volume": [10],
        }
    )

    result = BarchartPriceNormalizer.normalize(source)

    assert result.index.name == "Time"
    assert list(result.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert result.iloc[0].to_dict() == {
        "Open": 1.0,
        "High": 2.0,
        "Low": 0.5,
        "Close": 1.5,
        "Volume": 10.0,
    }
