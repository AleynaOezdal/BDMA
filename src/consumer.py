from confluent_kafka import Consumer
import os
from dotenv import load_dotenv
from producersetup import topic

load_dotenv()

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

c.close()