from confluent_kafka import Consumer
from database_setup import get_database
import json
import os
from dotenv import load_dotenv

load_dotenv()


def consume_messages(*args):
    dbname = get_database()
    collection_name = dbname["stock_price_lasthour"]

    c = Consumer(
        {
            "bootstrap.servers": os.getenv("BOOTSTRAP.SERVERS"),
            "security.protocol": os.getenv("SECURITY.PROTOCOL"),
            "sasl.mechanisms": os.getenv("SASL.MECHANISMS"),
            "sasl.username": os.getenv("SASL.USERNAME"),
            "sasl.password": os.getenv("SASL.PASSWORD"),
            "group.id": "group14",
            "auto.offset.reset": "earliest",
        }
    )

    c.subscribe(["stock_price_lasthour"])

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
