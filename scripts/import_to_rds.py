import csv
import getpass
import os
import ssl
from pathlib import Path

import pymysql

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

# Credentials are entered at runtime, never saved in the script.
host = input("RDS endpoint: ").strip()
username = input("MySQL username [admin]: ").strip() or "admin"
password = getpass.getpass("RDS password: ")

if not host:
    raise ValueError("RDS endpoint cannot be empty.")

# Require encrypted transport.
connection = pymysql.connect(
    host=host,
    port=3306,
    user=username,
    password=password,
    database="ecocart_db",
    charset="utf8mb4",
    ssl=ssl.create_default_context(
    cafile=str(ROOT / "database" / "rds-ca-bundle.pem")
),
    connect_timeout=15,
)

def load_csv(filename):
    with (DATA_DIR / filename).open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


try:
    products = load_csv("products.csv")
    customers = load_csv("customers.csv")

    with connection.cursor() as cursor:
        for product in products:
            cursor.execute(
                """
                INSERT INTO products
                (product_id, name, category, price, stock,
                 image_s3_key, description_s3_key)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    category = VALUES(category),
                    price = VALUES(price),
                    stock = VALUES(stock),
                    image_s3_key = VALUES(image_s3_key),
                    description_s3_key = VALUES(description_s3_key)
                """,
                (
                    product["product_id"],
                    product["name"],
                    product["category"],
                    product["price"],
                    product["stock"],
                    product["image_s3_key"],
                    product["description_s3_key"],
                ),
            )

        for customer in customers:
            cursor.execute(
                """
                INSERT INTO customers
                (customer_id, name, email, city)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    email = VALUES(email),
                    city = VALUES(city)
                """,
                (
                    customer["customer_id"],
                    customer["name"],
                    customer["email"],
                    customer["city"],
                ),
            )

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]

    print(f"Products in RDS: {product_count}")
    print(f"Customers in RDS: {customer_count}")
    print("CSV import completed successfully.")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
