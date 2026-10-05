# Automated Sales Data Pipeline

[🇧🇷 Português](README.md) | 🇺🇸 **English**

## About the project

This is a mini ETL pipeline developed in Python to validate, clean, standardize,
and consolidate sales spreadsheets received from multiple stores.

The project uses entirely fictional data and publicly demonstrates an automation
pattern that can reduce repetitive work before the data analysis stage.

## Business problem

A company periodically receives sales files from multiple stores. Before any
analysis can begin, someone must open each spreadsheet, check its columns,
identify invalid data, standardize categories, and consolidate all records.

Besides taking time, this manual process increases the risk of inconsistencies.
This project automates the following flow:

```text
Excel files → Extraction → Validation → Cleaning and standardization
             → Consolidation → Final Excel + rejections + log
```

## Objectives

- Automate the reading of multiple sales files.
- Validate spreadsheet schemas before processing.
- Identify inconsistent records and explain every rejection.
- Standardize categories and text fields.
- Calculate the total value of each sale automatically.
- Consolidate valid records only.
- Preserve traceability through source filenames and row numbers.
- Generate an execution summary and log file.

## Technologies

- Python 3.10+
- pandas
- openpyxl
- Excel
- logging

## Project structure

```text
automated-sales-data-pipeline/
├── data/
│   ├── input/
│   │   ├── sales_store_101.xlsx
│   │   ├── sales_store_102.xlsx
│   │   └── sales_store_103.xlsx
│   └── output/
├── logs/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── main.py
│   ├── transform.py
│   └── validate.py
├── .gitignore
├── generate_sample_data.py
├── README.md
├── README_EN.md
└── requirements.txt
```

## Validation rules

The pipeline checks:

- all eight required columns;
- unexpected columns;
- missing required values;
- duplicate sale IDs within one file;
- duplicate sale IDs across different files;
- store ID type and integrity;
- integer quantities greater than zero;
- numeric unit prices greater than zero;
- valid, non-future sale dates;
- categories included in the configured dictionary.

Variations such as `ELECTRONICS`, `electronics`, and `Eletrônicos` are mapped to
`Electronics`. Unknown categories are not changed silently: the record is
rejected and receives the corresponding explanation.

## Transformations

After validation, the pipeline removes unnecessary whitespace, standardizes
categories, converts numeric fields, normalizes dates, and creates `total_sale`:

```text
total_sale = quantity × unit_price
```

## How to run

Create and activate a virtual environment from the project root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies and run the pipeline:

```bash
pip install -r requirements.txt
python -m src.main
```

## Output

The main result is saved as `data/output/sales_consolidated.xlsx` and contains:

1. **Valid Sales** — clean, standardized, and consolidated records.
2. **Rejected Rows** — invalid records and their rejection reasons.
3. **Processing Summary** — processing status and row counts by file.

The technical execution history is saved as `logs/processing.log`.

## Demonstration results

| Metric | Result |
|---|---:|
| Files processed | 3 |
| Records analyzed | 13 |
| Valid records | 9 |
| Rejected records | 4 |

The deliberate errors are an unknown category, a zero quantity, a negative
unit price, and a future sale date. They demonstrate both the successful path
and the rejection workflow.

## Regenerate the fictional data

```bash
python generate_sample_data.py
```

## Skills demonstrated

- Python automation
- data manipulation with pandas
- ETL pipeline development
- data quality and business-rule validation
- error handling
- logging and traceability
- automated Excel reporting
- modular code organization
- technical documentation

## Privacy

All data in this repository is fictional. The project demonstrates a general
automation pattern without exposing employer data, internal code, or confidential
business rules.

## Author

**Alessandra Lira**  
Computer Science | Business Intelligence | Data Analytics

- [LinkedIn](https://www.linkedin.com/in/alessandra-lira-oliveira/)
- [GitHub](https://github.com/AlleLira)

