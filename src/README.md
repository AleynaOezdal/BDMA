# Our backend structure
### Here, we will provide all the files we have used for Task 1 and Task 2 to crawl data from the web, extract it, enrich it with ML methods and finally write them into our MongoDB Client.
---
#### :house: local_scraper

This is the directory for our local producer used for Task 1. They weren't used for Task 2 themselves, but rather served as a template for our cloud functions. 

#### :robot: kafka/producer

These are our producer running via Google Cloud Functions. Their structure is different to the local ones, which is due to slightly different requirements from GCP. We are producing our messages to a Kafka Cluster, managed by Confluent and running on GCP.

#### :bullettrain_front: kafka/consumer

We used Confluent Kafka for Event Streaming. These consumers read messages for corresponding Kafka topics and write them into our mongoDB client.


#### :brain: sentiment_analysis_spark

For the usage of Machine Learning Methods and Data Processing, we used Apache Spark to enrich our data with Artificial Intelligence (e.g. Classification). After the processing, we wrote the data into our mongoDB client.
