# EcoCart — Storage and Database Solution

**Cloud Computing | Modular Assignment 3**  
**AWS Region:** Europe (Stockholm), `eu-north-1`

## Quick links

- [Architecture diagram](docs/EcoCart-M3-Architecture.png)
- [Final assignment report](docs/Storage%20and%20Database%20Solution-M3-Report.docx)
- [Evidence screenshots](docs/evidence/)
- [Database schema](database/schema.sql)
- [Python scripts](scripts/)
- [Source datasets](data/)

## Project overview

EcoCart is a cloud storage and relational database demonstration for an e-commerce product catalog. It uses **Amazon RDS for MySQL** to store structured product and customer records and **Amazon S3** to store product images and text descriptions. Python scripts demonstrate database ingestion and S3 object retrieval.

The deployment was created for academic assessment. It is not a production e-commerce application.

## Architecture

[![EcoCart storage and database architecture](docs/EcoCart-M3-Architecture.png)](docs/EcoCart-M3-Architecture.png)

[Open the full-size architecture diagram](docs/EcoCart-M3-Architecture.png)

The Python scripts access the RDS database through a TLS-encrypted MySQL connection using database credentials. A separate Python script uses **boto3** with AWS credentials available in AWS CloudShell to list and read objects in S3. The `products` table stores S3 object keys that associate each product with its image and description; RDS does not connect directly to S3.

## AWS resources

| Resource | Configuration |
| --- | --- |
| Region | Europe (Stockholm), `eu-north-1` |
| Amazon RDS | MySQL 8.4, instance `ecocart-m3-mysql` |
| Database | `ecocart_db` |
| Database tables | `products` (10 records), `customers` (10 records) |
| Amazon S3 | Bucket `ecocart-m3-assets-habib` |
| S3 objects | 10 PNG images under `images/` and 10 TXT descriptions under `descriptions/` |
| RDS network access | Security group limited MySQL port 3306 to an authorized client IP during testing |
| RDS backup | Automated backups enabled; 1-day retention; automated snapshot verified |
| S3 protection | Block public access enabled; default SSE-S3 encryption |

> **Deployment status:** The infrastructure was deployed and tested for assessment. The RDS database was subsequently deleted as part of cost cleanup. The resource settings below describe the tested deployment, not currently running services.

## Repository structure

```text
EcoCart-Storage-Database/
├── data/
│   ├── products.csv
│   ├── customers.csv
│   ├── images/                 # P001.png–P010.png
│   └── descriptions/           # P001.txt–P010.txt
├── database/
│   ├── schema.sql
│   └── rds-ca-bundle.pem       # AWS RDS CA certificate bundle
├── scripts/
│   ├── generate_datasets.py
│   ├── generate_descriptions.py
│   ├── generate_images.py
│   ├── import_to_rds.py
│   └── verify_s3.py
├── docs/
│   ├── EcoCart-M3-Architecture.png
│   ├── evidence/               # Deployment and validation screenshots
│   └── Storage and Database Solution-M3-Report.docx
└── README.md
```

The completed assignment report is available in [`docs/Storage and Database Solution-M3-Report.docx`](docs/Storage%20and%20Database%20Solution-M3-Report.docx).

## Database design

The schema is defined in [`database/schema.sql`](database/schema.sql).

**`products`**

| Column | Type | Purpose |
| --- | --- | --- |
| `product_id` | `VARCHAR(10)` | Primary key |
| `name` | `VARCHAR(150)` | Product name |
| `category` | `VARCHAR(100)` | Product category |
| `price` | `DECIMAL(10,2)` | Nonnegative price |
| `stock` | `INT` | Nonnegative stock quantity |
| `image_s3_key` | `VARCHAR(255)` | Associated image object key |
| `description_s3_key` | `VARCHAR(255)` | Associated description object key |

**`customers`**

| Column | Type | Purpose |
| --- | --- | --- |
| `customer_id` | `VARCHAR(10)` | Primary key |
| `name` | `VARCHAR(150)` | Customer name |
| `email` | `VARCHAR(255)` | Unique email |
| `city` | `VARCHAR(100)` | Customer city |

The customer records are fictional test data using example email addresses.

## Python integration

### Import CSV data into RDS

Install the MySQL client library:

```bash
python -m pip install pymysql
```

While the RDS instance is running and its security group allows your current IP, run:

```bash
python scripts/import_to_rds.py
```

The script prompts for the RDS endpoint, MySQL username, and password; credentials are **not hardcoded**. The connection uses the AWS RDS CA certificate bundle for TLS verification. The import can be rerun without duplicating records because it uses upsert statements.

**Observed result:**

```text
Products in RDS: 10
Customers in RDS: 10
CSV import completed successfully.
```

### Verify S3 objects with boto3

Run the S3 verification script in an environment with configured AWS credentials, such as AWS CloudShell:

```bash
python3 -m pip install boto3
python3 scripts/verify_s3.py
```

The script lists image and description objects, retrieves `descriptions/P001.txt`, and validates that there are 10 PNG files and 10 TXT files. The S3 integration was successfully tested in AWS CloudShell. To run the repository script in CloudShell, first make the file available there.

## Security and backup controls

- **RDS:** MySQL access restricted by a security group to the authorized client IP on port 3306 during testing; TLS encryption with the AWS RDS CA bundle.
- **S3:** Public access blocked; objects private; SSE-S3 default encryption enabled.
- **Database constraints:** Primary keys, unique customer emails, and nonnegative price and stock checks.
- **Recovery:** RDS automated backups enabled with a one-day retention period; an available automated snapshot was verified in the AWS console.
- **Credentials:** Passwords and AWS access keys are not stored in project scripts or documentation.

## Validation and evidence

| Test | Result |
| --- | --- |
| RDS MySQL database and schema creation | Passed |
| Import products from CSV | Passed — 10 records |
| Import customers from CSV | Passed — 10 records |
| RDS SQL count verification | Passed — 10 records per table |
| S3 image object listing | Passed — 10 PNG files |
| S3 description object listing | Passed — 10 TXT files |
| S3 description retrieval using boto3 | Passed |
| RDS automated backup configuration | Verified — enabled, 1 day |

Evidence screenshots are retained in [`docs/evidence/`](docs/evidence/), including database deployment, S3 object organization, data verification, and backup configuration.

## Scope and limitations

This assignment demonstrates cloud storage, relational database configuration, programmatic data access, and security/backup settings. It does **not** implement a hosted web storefront, a production API, a multi-AZ RDS deployment, or an automated application-level end-to-end transaction spanning RDS and S3. RDS and S3 access were validated with separate Python workflows.

## Cost management

AWS resources may incur charges even on accounts with promotional credits. Following successful testing and submission, the RDS database was deleted. Remaining S3 objects, retained snapshots or backups, and billing should be reviewed and cleaned up as appropriate.

## Project references

- **Repository:** https://github.com/mdhabibhameedi/ecocart-storage-database-solution
- **Architecture:** [View diagram](docs/EcoCart-M3-Architecture.png)
- **Submitted report:** [Open Word report](docs/Storage%20and%20Database%20Solution-M3-Report.docx)
- **Implementation evidence:** [Browse screenshots](docs/evidence/)
- **SQL schema:** [View schema](database/schema.sql)
- **Python scripts:** [Browse scripts](scripts/)

> **Note:** The architecture diagram must be uploaded to `docs/EcoCart-M3-Architecture.png` for the embedded preview to render. Links assume the corresponding files are present in the repository.
