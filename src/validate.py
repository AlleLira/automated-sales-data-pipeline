"""Schema and row-level data quality validation."""

from dataclasses import dataclass

import pandas as pd

from src.config import CATEGORY_ALIASES, REQUIRED_COLUMNS
from src.transform import normalize_lookup_key


@dataclass
class ValidationResult:
    valid_rows: pd.DataFrame
    rejected_rows: pd.DataFrame
    checks: dict[str, int]


def validate_schema(dataframe: pd.DataFrame) -> tuple[bool, list[str], list[str]]:
    """Check required and unexpected columns, ignoring traceability fields."""
    business_columns = [
        column
        for column in dataframe.columns
        if column not in {"source_file", "source_row"}
    ]
    missing = [column for column in REQUIRED_COLUMNS if column not in business_columns]
    unexpected = [column for column in business_columns if column not in REQUIRED_COLUMNS]
    return not missing and not unexpected, missing, unexpected


def validate_rows(dataframe: pd.DataFrame) -> ValidationResult:
    """Validate each row and separate valid from rejected records."""
    checked = dataframe.copy()
    reasons: list[list[str]] = [[] for _ in range(len(checked))]

    def add_reason(mask: pd.Series, message: str) -> None:
        for position in range(len(checked)):
            if bool(mask.iloc[position]):
                reasons[position].append(message)

    required_values = checked[REQUIRED_COLUMNS].isna() | (
        checked[REQUIRED_COLUMNS].astype("string").apply(lambda col: col.str.strip()).eq("")
    )
    add_reason(required_values.any(axis=1), "missing required value")

    sale_id_clean = checked["sale_id"].astype("string").str.strip()
    add_reason(sale_id_clean.duplicated(keep=False), "duplicate sale_id")

    store_numeric = pd.to_numeric(checked["store_id"], errors="coerce")
    quantity_numeric = pd.to_numeric(checked["quantity"], errors="coerce")
    price_numeric = pd.to_numeric(checked["unit_price"], errors="coerce")
    date_parsed = pd.to_datetime(checked["sale_date"], errors="coerce")

    add_reason(store_numeric.isna() | (store_numeric % 1 != 0), "invalid store_id")
    add_reason(quantity_numeric.isna() | (quantity_numeric % 1 != 0), "invalid quantity")
    add_reason(quantity_numeric.notna() & (quantity_numeric <= 0), "quantity must be positive")
    add_reason(price_numeric.isna(), "invalid unit_price")
    add_reason(price_numeric.notna() & (price_numeric <= 0), "unit_price must be positive")
    add_reason(date_parsed.isna(), "invalid sale_date")
    add_reason(
        date_parsed.notna() & (date_parsed.dt.normalize() > pd.Timestamp.today().normalize()),
        "future sale_date",
    )

    category_keys = checked["category"].map(normalize_lookup_key)
    add_reason(~category_keys.isin(CATEGORY_ALIASES), "unknown category")

    checked["rejection_reason"] = ["; ".join(row_reasons) for row_reasons in reasons]
    invalid_mask = checked["rejection_reason"].ne("")

    valid = checked.loc[~invalid_mask].drop(columns="rejection_reason").copy()
    rejected = checked.loc[invalid_mask].copy()

    # Keep parsed numeric/date values so transformation receives consistent types.
    valid["store_id"] = store_numeric.loc[valid.index]
    valid["quantity"] = quantity_numeric.loc[valid.index]
    valid["unit_price"] = price_numeric.loc[valid.index]
    valid["sale_date"] = date_parsed.loc[valid.index]

    checks = {
        "input_rows": len(checked),
        "valid_rows": len(valid),
        "rejected_rows": len(rejected),
    }
    return ValidationResult(valid, rejected, checks)

