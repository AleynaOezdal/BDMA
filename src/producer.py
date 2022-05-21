from bs4 import BeautifulSoup as bs
import json
from producersetup import initialize_yf_tickers, all_companies, topic, delivery_report, get


def produce_news_headlines(companies: list=all_companies):
    # All news to be stored in a dictionary
    all_news = {}

    for company in companies:
        # Scrape finanzen.net for each company on news section
        base_url = f'https://www.finanzen.net/news/{company}-news'
        soup = bs(get(base_url), 'html.parser')

        # Store headlines for every company in a dictionary
        found_news = soup.find_all("a", attrs={"class": "teaser"})

        # Declare a counter to enumerate headlines for each company
        count = 0

        # Iterate over every headline and store it in the all_news dict with corresponding enumeration
        for headline in found_news:
            all_news[f"{company}_{count}"] = headline.text
            count += 1
            post = {f"{company}_{count}": headline.text}
            #p.produce(topic, json.dumps(post), callback=delivery_report)
            #p.flush()
        # print(f"+++ Finished Company: {company} +++\n")

    return print("DONE. Produced all headlines to Kafka.")

if __name__ == '__main__':
    # Next steps: Every headline as single message to KAFKA
    # WARN: Only start if kafka cluster is set up!
    produce_news_headlines()