import json

from confluent_kafka import Consumer
from consumers.KPIs.databasesetup_KPIs import get_database

dbname = get_database()
collection_name = dbname["company_description"]

c = Consumer({
    'bootstrap.servers' :'pkc-4ygn6.europe-west3.gcp.confluent.cloud:9092',
    'security.protocol' : 'SASL_SSL',
    'sasl.mechanisms' : 'PLAIN',
    'sasl.username' : '2CV6Y6RATV64WJHF',
    'sasl.password' : '6kLfk90tFiAMSX5awmnQUx8TptlbxNb25zUEObq9uJwY+6bZuIUl0KI71wNfwu7M',
    'group.id': 'mygroup0402',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['company_description'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

    collection_name.insert_one(json.loads(msg.value().decode('utf-8')))
c.close()