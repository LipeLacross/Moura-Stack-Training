from __future__ import annotations
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

def run_spark_job(input_path: str = "data/sample_sales.csv", output_path: str = "data/processed/sales_spark.parquet"):
    spark = (
        SparkSession.builder.appName("moura-spark-etl")
        .config("spark.sql.parquet.compression.codec", "snappy")
        .getOrCreate()
    )
    df = spark.read.option("header", True).csv(input_path, inferSchema=True)
    df = df.withColumn("quantity", col("quantity").cast("int"))
    df = df.withColumn("unit_price", col("unit_price").cast("double"))
    df = df.withColumn("total", expr("quantity * unit_price"))
    rows = df.count()
    df.write.mode("overwrite").parquet(output_path)
    spark.stop()
    return {"rows": rows, "dest": output_path}

if __name__ == "__main__":
    print(run_spark_job())
