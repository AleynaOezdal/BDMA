#Installieren von MongoDB https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/ (MAC)
#Starten von MongoDB, auch dort beschrieben
#Für Windows: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
#Spark runterladen
#PySpark-Mongodb connector jar package runterladen und in spark/jar ordner machen https://mvnrepository.com/artifact/org.mongodb.spark/mongo-spark-connector_2.12/3.0.1

#In diesem Dokument: uri (Zeile 28 und 29) gegen eigene Austauschen
#File über Konsole laufen lassen: pfad zu spark ordner/bin/spark-submit --master "local[4]"  \
#                    --conf "spark.mongodb.input.uri=mongodb://127.0.0.1/test.coll?readPreference=primaryPreferred" \
#                    --conf "spark.mongodb.output.uri=mongodb://127.0.0.1/test.coll" \
#					--packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
#                  mongodb.py



from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

working_directory = 'jars/*'

# For spark version >= 3.0

spark = SparkSession\
    .builder\
    .master('local')\
    .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/database01.sparktest')\
    .config('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/database01.sparktest')\
    .config('spark.driver.extraClassPath', working_directory) \
    .getOrCreate()


people = spark.createDataFrame([("JULIA", 50), ("Gandalf", 1000), ("Thorin", 195), ("Balin", 178), ("Kili", 77),
                            ("Dwalin", 169), ("Oin", 167), ("Gloin", 158), ("Fili", 178), ("Bombur", 22)], ["name", "age"])

people.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
df.select('*').where(col("age") == "178").show()
