from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv


load_dotenv()

# Load MongoDB URI from environment variables
uri = os.getenv('uri')

brokers = "localhost:9092"
topic = "reddit"

# Create Spark session with MongoDB configuration
spark = SparkSession.builder \
    .appName("RedditKafkaMongo") \
    .config("spark.master", "local[*]") \
    .config('spark.mongodb.output.uri', uri) \
    .config("spark.mongodb.output.database", os.getenv('database')) \
    .config("spark.mongodb.output.collection", os.getenv('collection')) \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.network.timeout", "600s") \
    .getOrCreate()  # Corrected method name

# Read data from Kafka topic 'reddit'
kafka_stream_df = spark.readStream \
                    .format('kafka') \
                    .option("kafka.bootstrap.servers", brokers) \
                    .option("subscribe", topic) \
                    .option("startingOffsets", "earliest") \
                    .load()

# Print schema to inspect the data structure
kafka_stream_df.printSchema()

# Convert the Kafka value (binary) to a string
kafka_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as data", "timestamp")
kafka_stream_df.printSchema()

# Write the processed stream to MongoDB
kafka_stream_df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch_id: df.write \
                  .format("mongo") \
                  .mode("append") \
                  .option("uri", uri) \
                  .option("database", os.getenv('database')) \
                  .option("collection", os.getenv('collection')) \
                  .save()) \
    .start() \
    .awaitTermination()