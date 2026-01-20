# README

## 1. Understand Files and foldes 

---

**Personal vs Upstream**

Personal folder 

- `/anancapital`

**Untracked files and folders** 

Untracked file

- `anancapita/private_config.yaml`


## 2. Modified core files

---

The following files differ from the original repository:

1. **Override mechanism added**

   * `bc-utils/bcutils/config.py`

2. **Append .gitignore**

   * `bc-utils/.gitignore`

3. **Add Normalisation: Converting Latest to Close** 
   * `bcutils/bc_utils.py`
   * `anancapital/normalization.py`

## 3. Project Initialization

---

### Step 1: Clone the original project

```bash
git clone https://github.com/bug-or-feature/bc-utils.git
```

### Step 2: Create personal workspace

Inside the project root, create a personal folder:

```text
anancapital/
├── private_config.yaml
├── private_contract_map.py
├── pst.py
└── README.md
```

### Step 3: Configure private settings

* Fill in `private_config.yaml`
* Ensure all private files are listed in `.gitignore`


## 4. Updating from Upstream

---

Period: Yearly

This process should be used whenever the original project adds or modifies instruments, exchanges, or logic.

### Step 1: Start from a clean `main`

```bash
git checkout main
git pull origin main
```

### Step 2: Fetch latest upstream changes

```bash
git fetch upstream
```

> This downloads updates from the original repository **without modifying your code**.

### Step 3: Create a sync branch

```bash
git checkout -b sync-upstream-YYYY-MM-DD
```

### Step 4: Merge upstream changes

```bash
git merge upstream/main
```

* Resolve conflicts if any
* Do **not** modify private files

### Step 5: Commit merged changes

```bash
git add -A
git commit -m "Sync upstream YYYY-MM-DD"
```

### Step 6: Test overrides

Verify that overrides work correctly:

```bash
python -m anancapital.print_contract_map
```

### Step 7: Run in production (recommended)

* Use the sync branch for ~1 month
* Monitor for missing instruments, roll issues, or data errors

### Step 8: Merge sync branch into `main`

```bash
git checkout main
git merge sync-upstream-YYYY-MM-DD
git push origin main
```

### Step 9: Clean up sync branch

```bash
git branch -d sync-upstream-YYYY-MM-DD
git push origin --delete sync-upstream-YYYY-MM-DD
```

## 5. Project Backup

---

Period: Quarterly 

1. Copy file untrack file: `private_config.yaml` to SSD in `bc-utils/anancapital/private_config-2025-01-01`


## 6. How to Use the Project

---

### Step 1: Initialize

Clone and configure the project as described above.

### Step 2: Set configuration

Edit `anancapital/private_config.yaml`

### Step 3: Download contract data

Run:

```bash
python anancapital/pst.py
```

### Step 4: Data storage

Downloaded CSV files are stored in:

```text
bc-utils/data
```

### Step 5: Convert CSV → Parquet

Run:

```bash
python pysystemtrade/program/initialize/convert_csv_to_parquet.py
```

Parquet files will be stored under:

```text
private-pysystemtrade/parquet
```


## 6. Notes & Caveats (Version 2025)

---

1. **Recommended download timing**

   * Download after market close (Saturday or Sunday)
   * Weekday downloads should only target completed contracts or months

2. **Incomplete data risk**

   * Partial data will cause downstream failures
   * Always verify full session coverage

3. **Time format**

   * All data is in **UTC**
   * Includes full trading sessions

4. **Download behavior**

   * Existing contracts are never overwritten

5. **Update limitations**

   * Update function works for **daily data**
   * Update function does **not** work for **hourly data**

6. **Roll configuration**

   * Roll logic uses `_PriceRollCycle_` from:

     * [https://github.com/robcarver17/pysystemtrade/blob/develop/data/futures/csvconfig/rollconfig.csv](https://github.com/robcarver17/pysystemtrade/blob/develop/data/futures/csvconfig/rollconfig.csv)

---
