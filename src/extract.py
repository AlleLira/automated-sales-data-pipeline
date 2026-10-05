"""File discovery and extraction functions."""

from pathlib import Path

import pandas as pd


def discover_excel_files(input_dir: Path) -> list[Path]:
    """Return input Excel files in deterministic order."""
    return sorted(
        path
        for path in input_dir.glob("*.xlsx")
        if not path.name.startswith("~$")
    )


def read_sales_file(file_path: Path) -> pd.DataFrame:
    """Read the first sheet and retain the source filename for traceability."""
    dataframe = pd.read_excel(file_path, engine="openpyxl")
    dataframe.columns = [str(column).strip() for column in dataframe.columns]
    dataframe["source_file"] = file_path.name
    dataframe["source_row"] = range(2, len(dataframe) + 2)
    return dataframe

