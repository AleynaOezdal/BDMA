from confluent_kafka import Consumer
import os
from dotenv import load_dotenv
from producersetup import topic
import findspark
from pyspark.sql import SparkSession


load_dotenv()
#findspark.init()
#spark = SparkSession.builder.master("local[*]").appName("pySparkBDMA").getOrCreate()

c = Consumer({
    'bootstrap.servers': os.getenv("BOOTSTRAP.SERVERS"),
    'security.protocol': os.getenv("SECURITY.PROTOCOL"),
    'sasl.mechanisms': os.getenv("SASL.MECHANISMS"),
    'sasl.username': os.getenv("SASL.USERNAME"),
    'sasl.password': os.getenv("SASL.PASSWORD"),
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe([f'{topic}'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error}")
        continue

    print(f"Received message: {msg.value().decode('utf-8')}")
    #simple_rdd = spark.sparkContext.parallelize(msg.value().decode('utf-8'))
    #print(simple_rdd.collect())

c.close()