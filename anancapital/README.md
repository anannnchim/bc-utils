# README

1. `private_config.yaml`
Use for setting up config

2. `pst`
- use for download data once, and set to update daily

3. bc-utils: `data/futures/contract_prices_csv`
- store csv data locally on my mac.

4. AnanCapitalFund: `src/data/parquet/futures_contract_prices`
- store parquet file in repo.

# Note

1. Make sure to download when market close, Sunday or Saturday
- Since it might contain un-complete data if not doing so.
- On weekday, just download old data or completed month.
- Make sure to include all data, if not it will fail later. 

2. Update function is not working for hour data but works for day.

3. Data is UTC format and contain full sessions.

4. Download function will not touch the pre-existed contract.

5. Update function is not wokring for HOUR data. 

6. In `config.py`, roll is _PriceRollCycle_ from
- https://github.com/robcarver17/pysystemtrade/blob/develop/data/futures/csvconfig/rollconfig.csv

7. After download all, we need move to `private/docs/event_process: Initialize new instrument data`  
# Untrack files
- `/Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_config.yaml`