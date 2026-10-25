import csv
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
data_dir = root / "data"

with (data_dir / "products.csv").open(
    newline="", encoding="utf-8-sig"
) as file:
    products = list(csv.DictReader(file))

for product in products:
    image_path = data_dir / product["image_s3_key"]
    image_path.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (800, 600), "#e8f1fa")
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (60, 60, 740, 540),
        radius=30,
        fill="#ffffff",
        outline="#2878b5",
        width=5
    )

    draw.text(
        (100, 200),
        product["name"],
        fill="#17324d"
    )

    draw.text(
        (100, 260),
        f"EcoCart Product: {product['product_id']}",
        fill="#2878b5"
    )

    image.save(image_path, "PNG")
    print(f"Created: {image_path.relative_to(root)}")

print(f"\nGenerated {len(products)} product images.")