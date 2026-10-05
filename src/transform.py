"""Cleaning and transformation functions."""

import re
import unicodedata

import pandas as pd

from src.config import CATEGORY_ALIASES


def _remove_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_lookup_key(value: object) -> str:
    """Create an accent-free, lowercase lookup key with normalized spacing."""
    text = "" if pd.isna(value) else str(value)
    text = _remove_accents(text).lower().strip()
    return re.sub(r"\s+", " ", text)


def clean_text(value: object) -> object:
    """Trim repeated whitespace while preserving missing values."""
    if pd.isna(value):
        return pd.NA
    return re.sub(r"\s+", " ", str(value).strip())


def standardize_category(value: object) -> object:
    """Map accepted category spellings to a canonical category."""
    key = normalize_lookup_key(value)
    return CATEGORY_ALIASES.get(key, pd.NA)


def transform_valid_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Apply business transformations to already validated rows."""
    transformed = dataframe.copy()

    for column in ["sale_id", "product", "seller"]:
        transformed[column] = transformed[column].map(clean_text)

    transformed["category"] = transformed["category"].map(standardize_category)
    transformed["store_id"] = transformed["store_id"].astype("int64")
    transformed["quantity"] = transformed["quantity"].astype("int64")
    transformed["unit_price"] = transformed["unit_price"].astype(float).round(2)
    transformed["sale_date"] = pd.to_datetime(transformed["sale_date"]).dt.normalize()
    transformed["total_sale"] = (
        transformed["quantity"] * transformed["unit_price"]
    ).round(2)

    return transformed[
        [
            "sale_id",
            "store_id",
            "product",
            "category",
            "quantity",
            "unit_price",
            "total_sale",
            "sale_date",
            "seller",
            "source_file",
            "source_row",
        ]
    ]

