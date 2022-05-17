import os
from dotenv import load_dotenv
from confluent_kafka import Producer


load_dotenv()
producer = Producer({
    'bootstrap.servers': os.getenv("BOOTSTRAP.SERVERS"),
    'security.protocol': os.getenv("SECURITY.PROTOCOL"),
    'sasl.mechanisms': os.getenv("SASL.MECHANISMS"),
    'sasl.username': os.getenv("SASL.USERNAME"),
    'sasl.password': os.getenv("SASL.PASSWORD")
})

topic = 'bdma'

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