from select import select
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, IntegerType, StringType

appName = "Kafka Examples"
master = "local"

spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .getOrCreate()

kafka_servers = "localhost:9092"

df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_servers) \
        .option("subscribe", "hannahtest1") \
        .option("startingOffsets", "earliest") \
        .load()

df.printSchema()

personStringDF = df.selectExpr("CAST(value AS STRING)")

schema = (
        StructType()
        .add("id", IntegerType())
        .add("name", StringType())
        .add("age", IntegerType())
    )

personDF = personStringDF.select(from_json(col("value"), schema).alias("data"))
info_df_fin = personDF.select("data.*")
#personDF = spark.createDataFrame(data = from_json(col("value"), schema), schema = schema)

info_df_fin.writeStream \
      .format("console") \
      .outputMode("append") \
      .start() \
      .awaitTermination()

