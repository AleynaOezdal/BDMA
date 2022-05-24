from confluent_kafka import Consumer
import os
from dotenv import load_dotenv
from static_scraper import financial_KPIs, get_kpi_topic

load_dotenv()


def create_consumers_for_topics(topics: list):
    all_messages_for_topic = list()
    for topic in topics:

        c = Consumer(
            {
                "bootstrap.servers": os.getenv("BOOTSTRAP.SERVERS"),
                "security.protocol": os.getenv("SECURITY.PROTOCOL"),
                "sasl.mechanisms": os.getenv("SASL.MECHANISMS"),
                "sasl.username": os.getenv("SASL.USERNAME"),
                "sasl.password": os.getenv("SASL.PASSWORD"),
                "group.id": topic,
                "auto.offset.reset": "earliest",
            }
        )

        c.subscribe([f'{get_kpi_topic(topic)}'])

        i = 0
        while i < 39:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error}")
                continue

            # Do something with message
            all_messages_for_topic.append(msg.value().decode('utf-8'))
            i += 1

        c.close()

    return all_messages_for_topic


if __name__ == "__main__":
    # create_consumers_for_topics(financial_KPIs[:-1])
    pass
