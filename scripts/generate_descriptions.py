import csv
from pathlib import Path

data_dir = Path("data")
description_dir = data_dir / "descriptions"
description_dir.mkdir(parents=True, exist_ok=True)

descriptions = {
    "P001": "Ergonomic wireless mouse designed for comfortable everyday use.",
    "P002": "Mechanical keyboard with responsive switches for typing and gaming.",
    "P003": "Multiport USB-C hub for connecting displays and USB accessories.",
    "P004": "Adjustable laptop stand for improved desk ergonomics.",
    "P005": "Portable Bluetooth speaker with clear audio and wireless connectivity.",
    "P006": "Durable travel backpack with organized storage compartments.",
    "P007": "Reusable water bottle suitable for everyday hydration.",
    "P008": "Adjustable desk lamp designed for home office lighting.",
    "P009": "Notebook set for writing, studying, and organizing notes.",
    "P010": "Compact phone holder for convenient hands-free viewing."
}

with (data_dir / "products.csv").open(
    newline="", encoding="utf-8-sig"
) as file:
    products = list(csv.DictReader(file))

for product in products:
    product_id = product["product_id"]
    output_path = data_dir / product["description_s3_key"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        descriptions[product_id],
        encoding="utf-8"
    )

    print(f"Created: {output_path}")

print(f"\nSuccessfully created {len(products)} product descriptions.")
