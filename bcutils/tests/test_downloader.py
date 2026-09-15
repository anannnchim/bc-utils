import asyncio
import os
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pandas as pd
import pytest

from bcutils.bc_utils import (
    Resolution,
    get_barchart_downloads,
    create_bc_session,
    save_prices_for_contract,
    HistoricalDataResult,
    _build_save_path,
    _get_contract_month_year,
    _get_start_end_dates,
    _get_exchange_for_code,
    _historical_prices_predicate,
    _save_download_and_cleanup,
    _update_barchart_contract_file_async,
)


@pytest.fixture(autouse=True)
def download_dir(tmp_path):
    download_dir = tmp_path / "prices"
    download_dir.mkdir()
    return download_dir.absolute()


@pytest.fixture()
def bc_config():
    config = {
        "barchart_username": "BARCHART_USERNAME",
        "barchart_password": "BARCHART_PASSWORD",
    }
    bc_config = {k: os.environ.get(v) for k, v in config.items() if v in os.environ}
    return bc_config


class TestDownloader:
    def test_contract_update_appends_without_rewriting_existing_rows(
        self, monkeypatch, tmp_path
    ):
        csv_path = tmp_path / "Day_S50-TFEX_20200900.csv"
        original = (
            "Time,Open,High,Low,Close,Volume\n"
            "2020-09-10T05:00:00+0000,1000,1010,990,1005,100\n"
            "2020-09-11T05:00:00+0000,1005,1015,995,1010,110\n"
        )
        csv_path.write_text(original)
        update = pd.DataFrame(
            {
                "Open": [1005.0, 1010.0, 1015.0],
                "High": [1015.0, 1020.0, 1025.0],
                "Low": [995.0, 1000.0, 1005.0],
                "Close": [1010.0, 1015.0, 1020.0],
                "Volume": [110, 120, 130],
            },
            index=pd.to_datetime(
                [
                    "2020-09-11T05:00:00+00:00",
                    "2020-09-12T05:00:00+00:00",
                    "2020-09-13T05:00:00+00:00",
                ]
            ),
        )
        update.index.name = "Time"
        fetch = AsyncMock(return_value=update)
        monkeypatch.setattr(
            "bcutils.bc_utils._get_historical_prices_for_contract_async", fetch
        )

        asyncio.run(
            _update_barchart_contract_file_async(
                human=None,
                contract_map={
                    "S50-TFEX": {
                        "code": "TE",
                        "cycle": "HMUZ",
                        "exchange": "TFEX",
                    }
                },
                path=str(tmp_path),
                contract_id="TEU20",
                res=Resolution.Day,
            )
        )

        result = csv_path.read_text()
        assert result.startswith(original)
        assert len(result.splitlines()) == 5

    def test_historical_response_must_match_requested_contract(self):
        predicate = _historical_prices_predicate(Resolution.Day, "TEH26")

        matching_response = SimpleNamespace(
            request=SimpleNamespace(
                method="GET",
                url=(
                    "https://www.barchart.com/proxies/timeseries/historical/"
                    "queryeod.ashx?symbol=TEH26&data=daily&volume=contract"
                ),
            )
        )
        stale_response = SimpleNamespace(
            request=SimpleNamespace(
                method="GET",
                url=(
                    "https://www.barchart.com/proxies/timeseries/historical/"
                    "queryeod.ashx?symbol=U1Z25&data=daily&volume=contract"
                ),
            )
        )

        assert predicate(matching_response)
        assert not predicate(stale_response)

    def test_saved_download_removes_browser_temp_file(self, tmp_path):
        download = AsyncMock()
        save_path = str(tmp_path / "Day_JPY_20261200.csv")

        asyncio.run(_save_download_and_cleanup(download, save_path))

        download.save_as.assert_awaited_once_with(save_path)
        download.delete.assert_awaited_once_with()

    def test_no_credentials(self, download_dir):
        with pytest.raises(Exception):
            get_barchart_downloads(
                create_bc_session(config_obj={}),
                contract_map={
                    "AUD": {"code": "A6", "cycle": "HMUZ", "exchange": "CME"}
                },
                save_dir=str(download_dir.absolute()),
                start_year=2020,
                end_year=2022,
                dry_run=False,
            )

    def test_hourly(self, bc_config, download_dir):
        if not self._have_creds(bc_config):
            pytest.skip("Skipping test, no Barchart credentials found in env")
        else:
            get_barchart_downloads(
                create_bc_session(config_obj=bc_config),
                contract_map={"AUD": {"code": "A6", "cycle": "H", "exchange": "CME"}},
                save_dir=str(download_dir),
                start_year=2020,
                end_year=2021,
                dry_run=False,
                pause_between_downloads=False,
            )

            csv = download_dir / "Hour_AUD_20200300.csv"
            assert csv.exists()
            assert not csv.is_dir()

    def test_daily(self, bc_config, download_dir):
        if not self._have_creds(bc_config):
            pytest.skip("Skipping test, no Barchart credentials found in env")
        else:
            get_barchart_downloads(
                create_bc_session(config_obj=bc_config),
                contract_map={"AUD": {"code": "A6", "cycle": "H", "exchange": "CME"}},
                save_dir=str(download_dir),
                start_year=2020,
                end_year=2021,
                do_daily=True,
                dry_run=False,
                pause_between_downloads=False,
            )

            csv = download_dir / "Day_AUD_20200300.csv"
            assert csv.exists()
            assert not csv.is_dir()

    def test_insufficient(self, bc_config, download_dir):
        if not self._have_creds(bc_config):
            pytest.skip("Skipping test, no Barchart credentials found in env")
        else:
            contract_key = "UPU14"
            month, year = _get_contract_month_year(contract_key)
            save_path = _build_save_path(
                "CHFJPY", month, year, Resolution.Hour, os.getcwd()
            )
            start_date, end_date = _get_start_end_dates(month, year)

            result = save_prices_for_contract(
                session=create_bc_session(config_obj=bc_config),
                contract=contract_key,
                save_path=save_path,
                start_date=start_date,
                end_date=end_date,
            )

            assert result == HistoricalDataResult.INSUFFICIENT

    def test_get_exchange(self, bc_config):
        if not self._have_creds(bc_config):
            pytest.skip("Skipping test, no Barchart credentials found in env")
        else:
            exch = _get_exchange_for_code(
                create_bc_session(config_obj=bc_config), "GCF24"
            )
            assert exch == "COMEX"

    @staticmethod
    def _have_creds(config: dict):
        return (
            "barchart_username" in config
            and config["barchart_username"]
            and "barchart_password" in config
            and config["barchart_password"]
        )
