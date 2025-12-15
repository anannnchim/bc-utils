# README

## 1. Files

---

All files are tracked by github clone. 

Personal folders

- /Users/nanthawat/PycharmProjects/bc-utils/anancapital
- /Users/nanthawat/PycharmProjects/bc-utils/data

Modified files

1. Add/modify config for instruments

- /Users/nanthawat/PycharmProjects/bc-utils/bcutils/config.py


Untrakced files

1. Define instrument we want to download.

- /Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_config.yaml
     

## 2. How to initialize project 

---
1. Clone the project by running below in terminal 


```plantuml
git clone https://github.com/bug-or-feature/bc-utils.git
```

2. Create a personal folder called `anancapital` that copy from sample folder & create `README.md` 
```
private_config.yaml
pst.py
```

3. Fill data in `private_config.yaml`. And make sure we put it in gitignore 

## 3. How to update projects 
---

pending

## 4. How to backup projects

pending

## 5. How to use projects  
---

1. Initialize project 

2. Set config
- In `/Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_config.yaml`

3. Download contract data 
- Run `/Users/nanthawat/PycharmProjects/bc-utils/anancapital/pst.py`

4. Data will be stored in 
 -  `/Users/nanthawat/PycharmProjects/bc-utils/data`

5. Convert csv contract files to parquet 
   - Run `/Users/nanthawat/PycharmProjects/pysystemtrade/program/initialize/convert_csv_to_parquet.py`
   - Store in `/Users/nanthawat/PycharmProjects/bc-utils`


## 6. Note
---

**Old version**
1. Make sure to download when market close, Sunday or Saturday
   - Since it might contain un-complete data if not doing so.
   - On weekday, just download old data or completed month.
   - Make sure to include all data, if not it will fail later. 

2. Update function is not working for hour data but works for day.

3. Data is UTC format and contain full sessions.

4. Download function will not touch the pre-existed contract.

5. Update function is not wokring for HOUR data. 

6. In `bcutils/config.py`, roll is _PriceRollCycle_ from
- https://github.com/robcarver17/pysystemtrade/blob/develop/data/futures/csvconfig/rollconfig.csv
