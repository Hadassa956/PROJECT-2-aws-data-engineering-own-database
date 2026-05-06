# AWS Serverless Data Engineering Pipeline

## Project Objective
This project demonstrates an end-to-end serverless data pipeline on Amazon Web Services (AWS). It is designed to handle the ingestion, transformation, and cataloging of customer data to enable secure and efficient analytical querying. 

The primary goal is to showcase the implementation of modern data engineering best practices, including Infrastructure as Code (IaC), distributed data processing, columnar storage optimization, and secure state management. The pipeline enforces specific business rules, such as filtering out inactive records, standardizing date formats, and ensuring data quality before making it available for downstream analytics.

## Architecture Overview
The data flow follows a standard Data Lake architecture, strictly utilizing serverless components:

1. **Data Generation & Ingestion:** Synthetic customer data is generated locally via Python and uploaded directly to an Amazon S3 Landing Zone.
2. **Data Transformation (ETL):** An AWS Glue Job running a PySpark script reads the raw CSV data. It applies business logic to filter out customers with a "Pending" status, casts data types appropriately (e.g., string to DateType), and selects specific columns required for analysis.
3. **Optimized Storage:** The transformed dataset is written to an Amazon S3 Processed Zone in Parquet format.
4. **Data Cataloging:** An AWS Glue Crawler automatically scans the Processed Zone, infers the schema, and registers the table metadata in the AWS Glue Data Catalog.
5. **Analytics:** Amazon Athena utilizes the Data Catalog to execute standard SQL queries directly against the Parquet files in S3.

## Technology Stack and Architecture Justification

Every technology in this pipeline was selected based on scalability, cost-efficiency, and operational excellence:

* **Terraform (Infrastructure as Code):** Used to provision all AWS resources. IaC ensures the environment is reproducible, version-controlled, and transparent. 
* **Remote Backend (S3 + DynamoDB):** A Terraform backend was implemented using an S3 bucket to store the `.tfstate` securely and a DynamoDB table for State Locking. This prevents concurrent modifications and state corruption, a critical requirement for production-level team environments.
* **Amazon S3 (Data Lake Storage):** Chosen as the foundational storage layer due to its high durability, unlimited scalability, and low cost. It cleanly separates the raw layer (Landing) from the transformed layer (Processed).
* **AWS Glue & PySpark (ETL Processing):** Selected because it is a fully managed, serverless Spark environment. It eliminates the operational overhead of provisioning and managing clusters while providing the computational power necessary for distributed data processing.
* **Parquet Format:** Implemented during the write phase because it is a highly optimized columnar storage format. It significantly reduces S3 storage costs and drastically improves query performance in Amazon Athena by minimizing the amount of data scanned.
* **AWS Glue Crawler:** Used to automate schema discovery. It eliminates the need for manual DDL (Data Definition Language) operations and keeps the data catalog synchronized with the physical files in S3.
* **Amazon Athena (Analytics):** Chosen for its serverless, pay-per-query model. It allows immediate SQL analysis on data stored in S3 without the architectural complexity of loading data into a traditional relational data warehouse.

## Repository Structure
```text
The Terraform configuration follows modular best practices, separating variables, providers, and outputs into distinct files for maintainability.
```text
.
├── terraform-bootstrap/       # Directory containing infrastructure code for the remote backend (S3 & DynamoDB)
├── .gitignore                 # Version control exclusions to protect data and sensitive state files
├── .terraform.lock.hcl        # Terraform dependency lock file ensuring provider version consistency
├── backend.tf                 # Configures Terraform to utilize the remote backend (State Lock)
├── data_generator.py          # Python script to generate the synthetic customer dataset
├── etl_script.py              # PySpark script executed by the AWS Glue Job for data transformation
├── glue.tf                    # Specific Terraform configurations for AWS Glue (Jobs, Crawlers)
├── ingestion_s3.py            # Python script utilizing boto3 to upload raw data to the S3 Landing Zone
├── main.tf                    # Primary Terraform configuration for core resources (Data Lake buckets, IAM roles)
├── outputs.tf                 # Defines infrastructure outputs (e.g., generated bucket names, IAM role ARNs)
├── providers.tf               # AWS provider configurations and required Terraform versions
├── variables.tf               # Input variables for Terraform, making the infrastructure highly reusable
└── README.md                  # Comprehensive project documentation
