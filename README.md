Real-Time Ride-Sharing Analytics with Apache Spark
Overview
This project implements a real-time analytics pipeline for a ride-sharing platform using Apache Spark Structured Streaming. The pipeline ingests streaming ride data, performs real-time aggregations, and analyzes trends over time.

Workflow
A Python script simulates real-time ride-sharing data.

Apache Spark Structured Streaming ingests, cleans, and processes the data.

The processed results are stored in CSV files for further analysis.

Setup and Requirements
Prerequisites
Ensure you have the following installed:

Apache Spark (3.x)

Java 8 or higher

Python 3.x

PySpark

Netcat (for simulating streaming data)

A terminal or command prompt

Installing Dependencies
Run the following command to install required Python libraries:

pip install pyspark
Project Structure

/real-time-ride-sharing-analytics
│── data/                # Directory for storing CSV output files
│── task1_ingest.py   # Task 1: Data ingestion and parsing
│--- task2_aggregate.py # Task 2: Real-time aggregations
│--- task3_window.py    # Task 3: Time-based analytics
│── README.md             # Project documentation
Running the Project
Step 1: Start the Data Stream
Open a terminal and run the following command to simulate a ride-sharing data stream:

nc -lk 9999
Paste JSON-formatted ride data into the terminal for testing, such as:

json

{"trip_id": "T123", "driver_id": "D456", "distance_km": 12.5, "fare_amount": 25.0, "timestamp": "2025-04-01T14:30:00"}
Task 1: Streaming Ingestion and Parsing
Objective
Read streaming data from localhost:9999.

Parse JSON messages into a Spark DataFrame.

Display the data in real time.

Implementation
Run the following command:

python task1_ingest.py
Key Code Snippet
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

# Create Spark session
spark = SparkSession.builder.appName("RideSharingStream").getOrCreate()

# Define schema
schema = StructType() \
    .add("trip_id", StringType()) \
    .add("driver_id", StringType()) \
    .add("distance_km", DoubleType()) \
    .add("fare_amount", DoubleType()) \
    .add("timestamp", StringType())

# Read streaming data
stream_df = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()

# Parse JSON
parsed_df = stream_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Output to console
query = parsed_df.writeStream.outputMode("append").format("console").start()
query.awaitTermination()
Task 2: Real-Time Aggregations
Objective
Compute total fare per driver.

Compute average trip distance per driver.

Write the results to CSV files.

Implementation
Run the following command:

python task2_aggregate.py
Key Code Snippet

from pyspark.sql.functions import avg, sum

# Aggregate Data
agg_df = parsed_df.groupBy("driver_id").agg(
    sum("fare_amount").alias("total_fare"),
    avg("distance_km").alias("avg_distance")
)

# Write results to CSV
query = agg_df.writeStream.outputMode("complete").format("csv").option("path", "data/aggregations").option("checkpointLocation", "data/checkpoint").start()
query.awaitTermination()
Task 3: Windowed Time-Based Analytics
Objective
Convert the timestamp column to TimestampType.

Compute a 5-minute moving window aggregation, sliding every 1 minute.

Write the results to CSV files.

Implementation
Run the following command:

python task3_window.py
Key Code Snippet

from pyspark.sql.functions import col, window
from pyspark.sql.types import TimestampType

# Convert timestamp column
parsed_df = parsed_df.withColumn("event_time", col("timestamp").cast(TimestampType()))

# Perform windowed aggregation
windowed_df = parsed_df.groupBy(window(col("event_time"), "5 minutes", "1 minute")).sum("fare_amount").alias("total_fare")

# Write results to CSV
query = windowed_df.writeStream.outputMode("complete").format("csv").option("path", "data/windowed").option("checkpointLocation", "data/checkpoint_window").start()
query.awaitTermination()
Expected Outputs
Console output for parsed ride data (Task 1).

CSV files containing aggregated driver earnings and distances (Task 2).

CSV files with 5-minute windowed fare analysis (Task 3).

Troubleshooting
Spark is not connecting to the socket: Ensure that Netcat is running (nc -lk 9999).

FileNotFoundError for checkpoint location: Create the necessary folders using mkdir -p data/checkpoint data/checkpoint_window.

Performance issues with large data streams: Try using Kafka instead of socket for better scalability.

Conclusion
By completing this project, you have implemented a real-time streaming analytics pipeline using Apache Spark Structured Streaming. You have gained hands-on experience with:
✅ Streaming data ingestion
✅ Real-time aggregations
✅ Time-windowed analytics