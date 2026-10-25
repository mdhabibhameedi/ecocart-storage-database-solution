import csv
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

products = [
    ["P001", "Wireless Mouse", "Electronics", "24.99", 120],
    ["P002", "Mechanical Keyboard", "Electronics", "79.99", 65],
    ["P003", "USB-C Hub", "Electronics", "39.50", 90],
    ["P004", "Laptop Stand", "Accessories", "32.00", 75],
    ["P005", "Bluetooth Speaker", "Electronics", "59.99", 40],
    ["P006", "Travel Backpack", "Bags", "49.99", 55],
    ["P007", "Water Bottle", "Lifestyle", "18.50", 200],
    ["P008", "Desk Lamp", "Home Office", "35.00", 80],
    ["P009", "Notebook Set", "Stationery", "12.99", 150],
    ["P010", "Phone Holder", "Accessories", "15.99", 110],
]

customers = [
    ["C001", "Aisha Khan", "aisha@example.com", "Riyadh"],
    ["C002", "Omar Ali", "omar@example.com", "Jeddah"],
    ["C003", "Sara Ahmed", "sara@example.com", "Dammam"],
    ["C004", "Zaid Hassan", "zaid@example.com", "Riyadh"],
    ["C005", "Mariam Noor", "mariam@example.com", "Mecca"],
    ["C006", "Bilal Farooq", "bilal@example.com", "Medina"],
    ["C007", "Huda Saleh", "huda@example.com", "Jeddah"],
    ["C008", "Yusuf Malik", "yusuf@example.com", "Riyadh"],
    ["C009", "Fatima Rahman", "fatima@example.com", "Abha"],
    ["C010", "Hamza Ibrahim", "hamza@example.com", "Taif"],
]

with (data_dir / "products.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "product_id", "name", "category", "price", "stock",
        "image_s3_key", "description_s3_key"
    ])
    for product_id, name, category, price, stock in products:
        writer.writerow([
            product_id, name, category, price, stock,
            f"images/{product_id}.png",
            f"descriptions/{product_id}.txt"
        ])

with (data_dir / "customers.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id", "name", "email", "city"])
    writer.writerows(customers)

print("Created data/products.csv with 10 products.")
print("Created data/customers.csv with 10 customers.")
