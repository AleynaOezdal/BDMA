import pyspark
import sparknlp
from pyspark.sql import SparkSession
from sparknlp.base import *
from sparknlp.annotator import *
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as F
import os
from dotenv import load_dotenv

load_dotenv()

# Verbindung zu unserem MongoDB Cluster
connectionString = f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/"

# Konfiguration von pyspark
conf = pyspark.SparkConf()
conf.set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector:10.0.2,com.johnsnowlabs.nlp:spark-nlp_2.12:3.4.4")

# SparkSession mit allen benötigten Konfigurationen (MongoDB und SparkNLP) erstellen
spark = SparkSession.builder \
    .appName("Spark NLP")\
    .master("local[4]")\
    .config("spark.driver.memory","16G") \
    .config("spark.driver.maxResultSize", "0") \
    .config("spark.kryoserializer.buffer.max", "2000M")\
    .config('spark.mongodb.read.connection.uri', connectionString)\
    .config('spark.mongodb.write.connection.uri', connectionString)\
    .config(conf=conf) \
    .getOrCreate()

# Auslesen der Collection company_news in Spark DataFrame
df = spark.read.format("mongodb").option("database", "Company-Experience").option("collection", "company_news").load()

# DataFrame in gewünschte Struktur bringen, Verschachtelungen glätten
df2 = df.select(col("_id"),
    col("news.more_info"),
    col("news.headline"),
    col("news.timestamp"),
    col("time"))
df2Flatten = df2.toDF("id","more_info","message","time","timestamp")

# SparkNLP Model Pipeline:
document = DocumentAssembler() \
    .setInputCol("message") \
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

empty_df = spark.createDataFrame([['']]).toDF("text")

pipelineModel = nlpPipeline.fit(empty_df)

result = pipelineModel.transform(df2Flatten)

df_results = result.select(col("id"),
    col("more_info"),
    col("message"),
    col("time"),
    col("timestamp"),
    col("class.result"))

df_resultsFlatten = df_results.toDF("id", "more_info", "message", "time", "timestamp", "class")

finished_df = df_resultsFlatten.withColumn('class', F.explode('class'))
finished_df.show()

finished_df.write.format("mongodb").mode("append").option("database", "Company-Experience").option("collection", "company_news_sentiment").save()

