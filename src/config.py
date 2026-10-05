"""Central configuration for the sales data pipeline."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_FILE = OUTPUT_DIR / "sales_consolidated.xlsx"
LOG_FILE = LOG_DIR / "processing.log"

REQUIRED_COLUMNS = [
    "sale_id",
    "store_id",
    "product",
    "category",
    "quantity",
    "unit_price",
    "sale_date",
    "seller",
]

# Accepted spellings are normalized to the public value on the right.
CATEGORY_ALIASES = {
    "electronics": "Electronics",
    "electronic": "Electronics",
    "eletronicos": "Electronics",
    "eletronico": "Electronics",
    "furniture": "Furniture",
    "furnitures": "Furniture",
    "moveis": "Furniture",
    "office supplies": "Office Supplies",
    "office supply": "Office Supplies",
    "material de escritorio": "Office Supplies",
    "accessories": "Accessories",
    "accessory": "Accessories",
    "acessorios": "Accessories",
}

TEXT_COLUMNS = ["sale_id", "product", "category", "seller"]

