from select import select
import pyspark
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, IntegerType, StringType, BinaryType, StructField, ArrayType
from pyspark.shell import spark
import pyspark.sql.functions as F
from pyspark.sql.types import StringType
from sparknlp.annotator import *
from sparknlp.base import *
from pyspark.ml import Pipeline
import os
import sparknlp

confluentBootstrapServers = {bootstrap-server}
confluentApiKey = {apikey}
confluentSecret = {secret}

# Verbindung zu unserem MongoDB Cluster
connectionString = "mongodb+srv://{username}:{password}@cluster0.hj2sr.mongodb.net/"
import sparknlp
spark = sparknlp.start()

# SparkNLP Model Pipeline:
document = DocumentAssembler() \
    .setInputCol("review") \
    .setOutputCol("document")

embeddings = BertSentenceEmbeddings\
    .pretrained('labse', 'xx') \
    .setInputCols(["document"]) \
    .setOutputCol("sentence_embeddings")

sentimentClassifier = ClassifierDLModel.pretrained("classifierdl_bert_sentiment", "de") \
    .setInputCols(["document", "sentence_embeddings"]) \
    .setOutputCol("class")

nlpPipeline = Pipeline(stages=[
 document,
 embeddings,
 sentimentClassifier
 ])


clickstreamTestDf = (
  spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", confluentBootstrapServers)
  .option("kafka.security.protocol", "SASL_SSL")
  .option("kafka.sasl.jaas.config", "org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(confluentApiKey, confluentSecret))
  .option("kafka.ssl.endpoint.identification.algorithm", "https")
  .option("kafka.sasl.mechanism", "PLAIN")
  .option("subscribe", "CustExp_functiontest")
  .option("failOnDataLoss", "false")
  .option("startingOffsets", "earliest")
  .load()
)

newsStringDF = clickstreamTestDf.selectExpr("CAST(value AS STRING)")


schema = (
        StructType()
        .add("_id", StringType())
        .add("customer_exp", StructType()
             .add("title", StringType())
             .add("review", StringType())
             .add("time", StringType())
             .add("more info", StringType()))
        .add("time", StringType())
    )

newsDF = newsStringDF.select(from_json(col("value"), schema).alias("data"))
headlinesdf = newsDF.select("data.*")
headlinesdf.printSchema()

df2 = headlinesdf.select(col("_id"),
    col("customer_exp.more info"),
    col("customer_exp.review"),
    col("customer_exp.title"),
    col("customer_exp.time"),
    col("time"))
df2Flatten = df2.toDF("id","more_info","review","title","time","timestamp")

empty_df = spark.createDataFrame([['']]).toDF("text")

pipelineModel = nlpPipeline.fit(empty_df)

result = pipelineModel.transform(df2Flatten)

df_results = result.select(col("id"),
    col("more_info"),
    col("review"),
    col("title"),
    col("time"),
    col("timestamp"),
    col("class.result"))

df_resultsFlatten = df_results.toDF("id", "more_info", "review", "title", "time", "timestamp", "class")

finished_df = df_resultsFlatten.withColumn('class', F.explode('class'))

finished_df.writeStream \
    .format("mongodb")\
    .option("spark.mongodb.connection.uri", connectionString) \
    .option("spark.mongodb.database", "Company-Experience") \
    .option("spark.mongodb.collection", "Customer_exp_GCP") \
    .option("checkpointLocation", "firstsparktest_1/checkpoint") \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
