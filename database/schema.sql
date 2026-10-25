CREATE DATABASE IF NOT EXISTS ecocart_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ecocart_db;

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    image_s3_key VARCHAR(255) NOT NULL,
    description_s3_key VARCHAR(255) NOT NULL,
    CONSTRAINT chk_product_price CHECK (price >= 0),
    CONSTRAINT chk_product_stock CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL
);
