"""Generate the fictional Excel inputs used to demonstrate the pipeline."""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd


INPUT_DIR = Path(__file__).resolve().parent / "data" / "input"


def build_sample_files() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today()

    files = {
        "sales_store_101.xlsx": [
            ["S101-001", 101, "Mouse Gamer", " electronics ", 2, 120.00, today - timedelta(days=6), "Ana"],
            ["S101-002", 101, "Mechanical Keyboard", "ELECTRONICS", 1, 250.00, today - timedelta(days=5), "Carlos"],
            ["S101-003", 101, "Office Chair", "Furniture", 1, 850.00, today - timedelta(days=4), "Ana"],
            ["S101-004", 101, "Notebook Stand", "accessories", 3, 89.90, today - timedelta(days=3), "Bruna"],
        ],
        "sales_store_102.xlsx": [
            ["S102-001", 102, "USB-C Cable", "Accessories", 5, 49.90, today - timedelta(days=6), "Diego"],
            ["S102-002", 102, "Desk Lamp", "office supplies", 2, 135.50, today - timedelta(days=5), "Elisa"],
            ["S102-003", 102, "Monitor 24", "Eletrônicos", 2, 899.00, today - timedelta(days=2), "Diego"],
            ["S102-004", 102, "Bookcase", "Móveis", 1, 620.00, today - timedelta(days=1), "Fernanda"],
        ],
        # Four deliberately invalid rows demonstrate the rejection rules.
        "sales_store_103.xlsx": [
            ["S103-001", 103, "Webcam", "Electronic", 2, 310.00, today - timedelta(days=4), "Gabriel"],
            ["S103-002", 103, "Headset", "Gaming", 1, 280.00, today - timedelta(days=3), "Helena"],
            ["S103-003", 103, "Desk Organizer", "Office Supply", 0, 75.00, today - timedelta(days=2), "Gabriel"],
            ["S103-004", 103, "HDMI Cable", "Accessories", 2, -35.00, today - timedelta(days=1), "Helena"],
            ["S103-005", 103, "Ergonomic Cushion", "Accessories", 2, 99.90, today + timedelta(days=3), "Igor"],
        ],
    }

    columns = [
        "sale_id",
        "store_id",
        "product",
        "category",
        "quantity",
        "unit_price",
        "sale_date",
        "seller",
    ]
    for filename, rows in files.items():
        pd.DataFrame(rows, columns=columns).to_excel(
            INPUT_DIR / filename, index=False, engine="openpyxl"
        )


if __name__ == "__main__":
    build_sample_files()
    print(f"Sample files created in: {INPUT_DIR}")

