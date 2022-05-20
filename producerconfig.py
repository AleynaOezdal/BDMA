from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import json

p = KafkaProducer(bootstrap_servers=['localhost:9092'], key_serializer=str.encode, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# produce keyed messages to enable hashed partitioning
#producer.send('scripttest', key=b'foo', value=b'bar')


topic = 'headlines'


def acked(err, msg):
    global delivered_records
    """Delivery report handler called on
    successful or failed delivery of message
    """
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))