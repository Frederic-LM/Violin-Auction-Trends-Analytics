# Violin Auction Trends Analytics

Companion code and data for the paper *The Verdict Never Rendered: Construct Validity, Non-Stationarity, and Selection in Two Centuries of Old-Versus-New Violin Trials* (F. Levi Mazloum, submitted per review, 2026). Interactive results: https://www.ruederome.com/trend.php

This repository provides the estimator, the derived per-maker results, and a data template for measuring the long-run real price performance of historical violin makers. It is designed so that any reader can reproduce the analysis from publicly available auction records.

---

## Data provenance and scope

The dataset of individual auction results used in the paper was **compiled by the author from publicly available auction results** (hammer prices, lot descriptions, sale dates), which auction houses disclose at the time of sale. The compiled transaction file is **not redistributed** in this repository. What is provided here is sufficient to reproduce the analysis from equivalent public sources:

- the estimator (`analyze.py`) and supporting tools;
- the **derived** results the paper cites (`maker_cagr_master_list.csv`) — per-maker aggregates only (computed CAGRs, sale counts, spans), containing no transaction-level prices;
- the biographical metadata (`makers_meta.json`);
- an empty **data template** (`all_violin_sales_template.csv`) showing the input schema.

To reproduce or extend the analysis, assemble your own transaction file from public auction records, format it to the template schema, and run `analyze.py`. The maker-ID system used here follows Tarisio's public numerical index (a numbering convention, not redistributed data); see below.

---

## 1. Design philosophy: why numerical maker IDs

Matching historical maker names across sources is error-prone — spelling variants, accents, and translation differences routinely split one maker's sales across several records. To make the pipeline robust, every transaction is anchored to a standardized integer `maker_id` rather than a name string.

The project uses Tarisio's public numerical indexing as that baseline. Storing rows by integer ID ensures name variants do not fragment a maker's record, and lets results be logged directly from public archives without a custom name-translation layer.

```
[ all_violin_sales.csv ]  <-- linked via maker_id -->  [ makers_meta.json ]
  maker_id (int)                                          maker_id (int)
  USD / EUR / GBP (price)                                 maker_name, country
  Sale Date (year)                                        birth, death, century
  Type (optional)                                         bio (optional)
```

The metadata in `makers_meta.json` extends the bare ID index: birth/death years cross-referenced against luthiery dictionaries and corrected where auction records disagreed, plus country and century classifications (which the bare index does not provide) to enable macro-level analysis.

---

## 2. Method (`analyze.py`)

The script estimates inflation-adjusted real growth for **deceased** makers with a settled sale record, via OLS log-regression of real price on sale year.

1. **Input.** Loads an auction CSV (searched in order: `auction_data_enhanced.csv`, `all_violin_sales.csv`, `auction_data.csv`) and `makers_meta.json`. Standardizes `maker_id` to integer; excludes bows if a `Type` column is present; parses currency values to numeric.
2. **Active span.** `Start_Active = birth + 25` (default 1500 if birth unknown); `End_Active = death`, or `birth + 85` if death unknown. `Is_Dead = True` if a death year exists or `birth + 85 < 2026`. Sales before `Start_Active` are dropped as misattributions.
3. **Century.** A manual `century` value in the JSON is respected and preserved; if missing, a fallback is derived as `(birth + 35) // 100 + 1`.
4. **Inflation adjustment.** Raw prices are deflated to constant 2026 currency using the selected index (CPI by default).
5. **Growth model.** Groups by maker; keeps makers meeting the liquidity filter (default **≥ 10 sales over ≥ 15 years**); fits `np.polyfit` OLS to ln(real price) vs. year for the Real CAGR (a nominal rate is computed alongside).
6. **Output.** Text summaries, Markdown reports (`violin_market_statistics.md`, `market_report.md`), the master results CSV (`maker_cagr_master_list.csv`), and Matplotlib plots.

---

## 3. Data pipeline: raw entry to analysis

Raw collection and final analysis are deliberately separated to protect data integrity.

```
[record_sales.py] -> YYYY-MM-DD_violin_sale_RAW.csv  (hammer price + currency; USD column blank)
        |
        v
[manual spreadsheet step] -> add buyer's premium, convert to USD
        |
        v
   all_violin_sales.csv
        |
        v
   [analyze.py] -> real-CAGR OLS models + reports
```

**Step 1 — `record_sales.py`.** Enter auction catalogue results; choose the session currency (USD / EUR / GBP). Entries are written to `Hammer Price` and `Currency`, leaving the `USD` column blank. Output is versioned per day (`_1.csv`, `_2.csv`, …) so nothing is overwritten.

**Step 2 — spreadsheet.** Open the raw CSV and populate `USD` as `USD = Hammer Price × (1 + buyer's premium) × exchange rate`. Save as `all_violin_sales.csv` in the repository root.

---

## 4. File formats

### `all_violin_sales.csv` (input — columns marked `*` are required by `analyze.py`)

| Column | Format | Notes |
| :-- | :-- | :-- |
| `maker_id` * | integer | matches key in `makers_meta.json` |
| `maker_name` | string | reference helper |
| `Sale Date Standard` * | `YYYY-MM-DD` (or 4-digit year) | transaction timing |
| `USD` * | integer / blank | processed USD value incl. premium |
| `EUR`, `GBP` | integer / blank | optional |
| `Type` | string | used for bow exclusion |
| `Auction House` | string | ignored by analytics |
| `Hammer Price` | integer | original nominal value |
| `Currency` | string | unit selected at recording |
| `Comment` | string | lot notes |

A minimal file needs only `maker_id`, `USD` (or `EUR`), and a date column.

```csv
maker_id,maker_name,Sale Date Standard,USD,EUR,GBP,Type,Auction House,Hammer Price,Currency,Comment
1042,Giuseppe Pedrazzini,2018-05-12,61200,,,Violin,Tarisio,45000,EUR,Sartory cert.
2081,Charles Jean Baptiste Collin-Mezin,1995-04-15,22350,,,Cello,Vichy,12500,GBP,Original pegs.
```

### `makers_meta.json` (metadata — JSON array of objects)

`maker_id` (int), `maker_name` (str), `country` (str), `birth` / `death` (int or null), `century` (str or null — **manual value takes precedence in analysis**), `bio` (str or null).

```json
[
  {
    "maker_id": 1042,
    "maker_name": "Giuseppe Pedrazzini",
    "country": "Italy",
    "century": "20",
    "birth": 1879,
    "death": 1957,
    "bio": "Worked primarily in Milan."
  }
]
```

### `maker_cagr_master_list.csv` (output)

Per-maker aggregates: `maker_id, maker_name, country, century, N_Sales, Span_Years, First_Sale, Last_Sale, Real_CAGR_%, Is_Dead`. No transaction-level prices.

---

## 5. Metadata tool (`up_meta.py`)

A command-line utility to safely view, add, or edit records in `makers_meta.json`.

- **Normalization.** If the JSON is an object keyed by ID, it is converted to the list-of-objects form `analyze.py` expects, injecting `maker_id`.
- **Lookup.** Prompts for a numeric maker ID with safe type-casting.
- **Editing.** New IDs prompt for all fields; existing IDs show current values, and pressing Enter keeps a value unchanged.
- **Century.** Writes a computed century rather than a blank: `"Unknown"` if no birth year; `"21"` if born after 1950 (unless a death year before 2000 gives `"20"`); otherwise `(birth + 35) // 100 + 1`.
- **Safe save.** Sorts by `maker_id` and writes UTF-8 with 4-space indentation.

---

## 6. Requirements

Python 3.9+ with:

```
pandas
numpy
matplotlib
```

```bash
pip install -r requirements.txt
python analyze.py
```

---

## 7. Contributing

The database does not yet cover all maker IDs, and `bio` is often empty. Contributions are welcome:

1. Fork or branch the repository.
2. Update `makers_meta.json` (use `up_meta.py` to avoid formatting errors).
3. Open a pull request.

Corrections to dates, countries, or missing makers are especially useful.

---

## License

Mozilla Public License 2.0. See `LICENSE`. © 2026 Frédéric Levi Mazloum.
