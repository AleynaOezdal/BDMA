from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType
import pyspark.sql.functions as F
from pyspark.sql.types import StringType
from sparknlp.annotator import *
from sparknlp.base import *
from pyspark.ml import Pipeline
import os
from dotenv import load_dotenv

# Setup Confluent Zugangsdaten
confluentBootstrapServers = os.getenv('BOOTSTRAP.SERVERS')
confluentApiKey = os.getenv('SASL.USERNAME')
confluentSecret = os.getenv('SASL.PASSWORD')

# Verbindung zu unserem MongoDB Cluster
connectionString = f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@bdma.rvryhyj.mongodb.net/"

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

# Starten des Readstreams mit Datenquelle Kafka
clickstreamTestDf = (
  spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", confluentBootstrapServers)
  .option("kafka.security.protocol", "SASL_SSL")
  .option("kafka.sasl.jaas.config", "org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(confluentApiKey, confluentSecret))
  .option("kafka.ssl.endpoint.identification.algorithm", "https")
  .option("kafka.sasl.mechanism", "PLAIN")
  .option("subscribe", "customer_experience")
  .option("failOnDataLoss", "false")
  .option("startingOffsets", "earliest")
  .load()
)

newsStringDF = clickstreamTestDf.selectExpr("CAST(value AS STRING)")

# Daten in Schema laden
schema = (
        StructType()
        .add("company", StringType())
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

df2 = headlinesdf.select(col("company"),
    col("customer_exp.more info"),
    col("customer_exp.review"),
    col("customer_exp.title"),
    col("customer_exp.time"),
    col("time"))
df2Flatten = df2.toDF("company","more_info","review","title","time","timestamp")

empty_df = spark.createDataFrame([['']]).toDF("text")

# Pipeline anwenden
pipelineModel = nlpPipeline.fit(empty_df)

result = pipelineModel.transform(df2Flatten)

# Finales Dataframe aufbauen
df_results = result.select(col("company"),
    col("more_info"),
    col("review"),
    col("title"),
    col("time"),
    col("timestamp"),
    col("class.result"))

df_resultsFlatten = df_results.toDF("company", "more_info", "review", "title", "time", "timestamp", "class")

finished_df = df_resultsFlatten.withColumn('class', F.explode('class'))

# Write Stream in MongoDB mit Checkpoint Location um Exactly-once Verarbeitung zu gewährleisten
finished_df.writeStream \
    .format("mongodb")\
    .option("spark.mongodb.connection.uri", connectionString) \
    .option("spark.mongodb.database", "Company-Environment") \
    .option("spark.mongodb.collection", "customer_exp_gcp") \
    .option("checkpointLocation", "gs://firstsparktest_1/checkpointsentimentcustexp") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
