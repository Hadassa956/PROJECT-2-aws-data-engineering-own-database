import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession    
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import StructType, StructField, IntegerType,StringType, IntegerType, DateType

def main():
    # 1. Dynamic parameters for bucket names
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'BUCKET_LANDING', 'BUCKET_PROCESSED'])

   #activating glue context and spark session
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)

    landing_path = f"s3://{args['BUCKET_LANDING']}/customer_data.csv"
    processed_path = f"s3://{args['BUCKET_PROCESSED']}/clientes_curated/"

    # schema definition for the incoming CSV data
    custom_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone_number", StringType(), True),
        StructField("address", StringType(), True),
        StructField("date_of_birth", StringType(), True),  # will convert to DateType later
        StructField("registration_date", StringType(), True),  # will convert to DateType later
        StructField("plan", StringType(), True),
        StructField("status", StringType(), True),
        StructField("date_of_churn", StringType(), True),  # will convert to DateType later
        StructField("employee_id", IntegerType(), True)
    ])

    print("⬇️ [LOG] reading raw data from Landing Zone...")
    # reading csv with predefined schema to ensure data consistency and type safety from the start of the pipeline. This also helps in catching any schema-related issues early on.
    df = spark.read.csv(landing_path, header=True, schema=custom_schema)

    df = df.select("customer_id", "name", "date_of_birth", "registration_date", "status")
    print("⚙️ [LOG] Initializing transformations and data cleaning...")
    
    # (Method Chaining) and typing
    df_transformed = (
        df.dropDuplicates(["customer_id"]) # ensure that we only have unique customer records based on the 'id' field, which is crucial for maintaining data integrity and avoiding duplicates in our processed dataset.
          .filter(col("status") != "Pending")
          # Converting date strings to actual date types for better querying and analysis downstream. This also ensures that any date-related operations in the future will work correctly without type issues.
          .withColumn("date_of_birth", to_date(col("date_of_birth"), "yyyy-MM-dd"))
          .withColumn("registration_date", to_date(col("registration_date"), "yyyy-MM-dd"))
    )

    print("⬆️ [LOG] writing optimized data to the Processed bucket...")
    
    
    (
        df_transformed.write
        .mode("overwrite")
        .parquet(processed_path)
    )

    job.commit()
    print("✅ [LOG] Pipeline executed successfully!")

# ENTRY POINT (Modularization)
if __name__ == '__main__':
    main()