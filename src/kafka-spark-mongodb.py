from select import select
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, IntegerType, StringType

appName = "Kafka Examples"
master = "local"
working_directory = 'jars/*'

spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/database02.sparkmongodbtest')\
    .config('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/database02.sparkmongodbtest')\
    .config('spark.driver.extraClassPath', working_directory) \
    .getOrCreate()

kafka_servers = "localhost:9092"

df = spark.read \
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

info_df_fin.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

df_neu = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
df_neu.select('*').where(col("age") == "20").show()

