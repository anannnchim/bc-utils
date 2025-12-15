# README

## 1. File Structure & Tracking

---

### Tracked by Git (default)

All source files from the original repository are tracked via Git.

### Private files (not tracked by Git)

These files are **local-only** and must remain in `.gitignore`:

* `/Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_config.yaml`
* `/Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_contract_map.py`

### Personal folders (local only)

These folders are created and maintained locally:

* `/Users/nanthawat/PycharmProjects/bc-utils/data`
* `/Users/nanthawat/PycharmProjects/bc-utils/anancapital`

### Modified core files

The following files differ from the original repository:

1. **Override mechanism added**

   * `/Users/nanthawat/PycharmProjects/bc-utils/bcutils/config.py`

2. **Extended ignore rules**

   * `/Users/nanthawat/PycharmProjects/bc-utils/.gitignore`

---

## 2. Project Initialization

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

> This folder is **not tracked by Git** and is specific to your environment.

### Step 3: Configure private settings

* Fill in `private_config.yaml`
* Ensure all private files are listed in `.gitignore`

---

## 3. Updating the Project from Upstream

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

---

## 4. Project Backup

---

Period: Quarterly 

**Status:** Pending
(Recommend periodic external drive or cloud snapshot of `/data` and `/anancapital`)

---

## 5. How to Use the Project

---

### Step 1: Initialize

Clone and configure the project as described above.

### Step 2: Set configuration

Edit:

* `/Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_config.yaml`

### Step 3: Download contract data

Run:

```bash
python anancapital/pst.py
```

### Step 4: Data storage

Downloaded CSV files are stored in:

```text
/Users/nanthawat/PycharmProjects/bc-utils/data
```

### Step 5: Convert CSV → Parquet

Run:

```bash
python /Users/nanthawat/PycharmProjects/pysystemtrade/program/initialize/convert_csv_to_parquet.py
```

Parquet files will be stored under:

```text
/Users/nanthawat/PycharmProjects/bc-utils
```

---

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
