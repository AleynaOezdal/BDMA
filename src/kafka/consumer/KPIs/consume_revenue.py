import json
from confluent_kafka import Consumer
from database_setup import get_database
import os
from dotenv import load_dotenv

load_dotenv()

dbname = get_database()
collection_name = dbname["total_revenue"]


def consume_messages():

    c = Consumer(
        {
            "bootstrap.servers": os.getenv("BOOTSTRAP.SERVERS"),
            "security.protocol": os.getenv("SECURITY.PROTOCOL"),
            "sasl.mechanisms": os.getenv("SASL.MECHANISMS"),
            "sasl.username": os.getenv("SASL.USERNAME"),
            "sasl.password": os.getenv("SASL.PASSWORD"),
            "group.id": "grouprevenue",
            "auto.offset.reset": "earliest",
        }
    )

    c.subscribe(["total_revenue"])

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print("Received message: {}".format(msg.value().decode("utf-8")))
        collection_name.insert_one(json.loads(msg.value().decode("utf-8")))

    c.close()


consume_messages()
