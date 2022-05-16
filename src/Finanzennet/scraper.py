import requests
from bs4 import BeautifulSoup as bs
from confluent_kafka import Producer
import json
from dotenv import load_dotenv
import os

if __name__ == '__main__':

    load_dotenv()
    p = Producer({
        'bootstrap.servers': os.getenv("BOOTSTRAP.SERVERS"),
        'security.protocol': os.getenv("SECURITY.PROTOCOL"),
        'sasl.mechanisms': os.getenv("SASL.MECHANISMS"),
        'sasl.username': os.getenv("SASL.USERNAME"),
        'sasl.password': os.getenv("SASL.PASSWORD")
    })

    topic = 'hdm_messages'

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

    # Crawling web page with given URL
    def get(url):
        res = requests.get(url)
        if res.status_code == 200:
            return res.text.strip()
        else:
            return 'Error in URL Status Code'

    # Parsing html
    dax40_companies = ["adidas", "sap", "bmw"]

    for company in dax40_companies:
        base_url = f'https://www.finanzen.net/news/{company}-news'
        # print(f"Now following company: {company}")
        record_key = company
        soup = bs(get(base_url), 'html.parser')

        """# Top Headlines on website - status: tbd
        content = soup.find('span', attrs={"class": "teaser-headline"})
        # print(content.text)"""

        # List Headlines on website and produce to kafka topic
        found_news = soup.find_all("a", attrs={"class": "teaser"})
        count = 0
        for headline in found_news:
            p.poll(0)
            record_value = json.dumps({f"{company}_{count}": headline.text})
            print("Producing record: {}\t{}".format(record_key, record_value))
            p.produce(topic, key=record_key.encode('utf-8'), value=record_value.encode('utf-8'), on_delivery=acked, callback=delivery_report)
            count += 1
            # print(f"{headline.text}")
        print(f"+++ Finished Company: {company} +++\n")

    p.flush()
