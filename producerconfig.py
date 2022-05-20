from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import json

p = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    key_serializer=str.encode,
    value_serializer=lambda v: v.encode('utf-8')
)

topic = 'headlines'

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))