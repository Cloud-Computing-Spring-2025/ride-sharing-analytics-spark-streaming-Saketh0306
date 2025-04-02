from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, sum, avg, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Initialize Spark Session
spark = SparkSession.builder.appName("StreamingTaxiData").getOrCreate()

# Define schema for incoming JSON data
schema = StructType([
    StructField("trip_id", StringType(), True),
    StructField("driver_id", StringType(), True),
    StructField("distance_km", DoubleType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("timestamp", StringType(), True)
])

# Read streaming data from socket
raw_stream = spark.readStream.format("socket").option("host", "localhost").option("port", 9998).load()

# Parse JSON data
parsed_stream = raw_stream.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Convert timestamp column to TimestampType
parsed_stream = parsed_stream.withColumn("event_time", col("timestamp").cast(TimestampType()))

# Task 1: Print parsed data to console
query1 = parsed_stream.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", "output/parsed_stream/") \
    .option("checkpointLocation", "output/checkpoints/parsed_stream/") \
    .start()

# Await termination
query1.awaitTermination()