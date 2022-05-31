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
conf.set(
    "spark.jars.packages",
    "org.mongodb.spark:mongo-spark-connector:10.0.2,com.johnsnowlabs.nlp:spark-nlp_2.12:3.4.4",
)

# SparkSession mit allen benötigten Konfigurationen (MongoDB und SparkNLP) erstellen
spark = (
    SparkSession.builder.appName("Spark NLP")
    .master("local[4]")
    .config("spark.driver.memory", "16G")
    .config("spark.driver.maxResultSize", "0")
    .config("spark.kryoserializer.buffer.max", "2000M")
    .config("spark.mongodb.read.connection.uri", connectionString)
    .config("spark.mongodb.write.connection.uri", connectionString)
    .config(conf=conf)
    .getOrCreate()
)

# Auslesen der Collection community_news in Spark DataFrame
df = (
    spark.read.format("mongodb")
    .option("database", "Company-Experience")
    .option("collection", "Community_news")
    .load()
)

# DataFrame in gewünschte Struktur bringen, Verschachtelungen glätten
df2 = df.select(
    col("_id"),
    col("community_news.more info"),
    col("community_news.User"),
    col("community_news.message"),
    col("community_news.timestamp"),
    col("time"),
)
df2Flatten = df2.toDF("id", "more_info", "user", "message", "time", "timestamp")

# SparkNLP Model Pipeline:
document = DocumentAssembler().setInputCol("message").setOutputCol("document")

embeddings = (
    BertSentenceEmbeddings.pretrained("labse", "xx")
    .setInputCols(["document"])
    .setOutputCol("sentence_embeddings")
)

sentimentClassifier = (
    ClassifierDLModel.pretrained("classifierdl_bert_sentiment", "de")
    .setInputCols(["document", "sentence_embeddings"])
    .setOutputCol("class")
)

nlpPipeline = Pipeline(stages=[document, embeddings, sentimentClassifier])

# Leeren DataFrame für Ergebnisse erstellen
empty_df = spark.createDataFrame([[""]]).toDF("text")

# Pipeline auf leeren DataFrame fitten
pipelineModel = nlpPipeline.fit(empty_df)

# Pipeline auf DataFrame mit Daten anwenden
result = pipelineModel.transform(df2Flatten)

# DataFrame für Ergebnisse erstellen, welches an Datenbank gesendet werden kann: Enthält alle Infos wie EingangsDF plus Klasse
df_results = result.select(
    col("id"),
    col("more_info"),
    col("user"),
    col("message"),
    col("time"),
    col("timestamp"),
    col("class.result"),
)

df_resultsFlatten = df_results.toDF(
    "id", "more_info", "user", "message", "time", "timestamp", "class"
)

# Entfernen der eckigen Klammern um Klasse
finished_df = df_resultsFlatten.withColumn("class", F.explode("class"))
# finished_df.show()

# DataFrame in Datenbank schreiben, collection Community_news_sentiment
finished_df.write.format("mongodb").mode("append").option(
    "database", "Company-Experience"
).option("collection", "Community_news_sentiment").save()
