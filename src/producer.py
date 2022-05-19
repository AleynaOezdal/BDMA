import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf
import pprint as pp
import json
from producersetup import producer, topic, acked, delivery_report

# Source for DAX Symbols: https://de.wikipedia.org/wiki/DAX#Zusammensetzung
yfinance_symbols_dax_companies = ['ads', 'air', 'alv', 'bas', 'bayn', 'bmw', 'bnr',
             'con', '1cov', 'dtg', 'dher', 'dbk', 'db1', 'dpw',
             'dte', 'eoan', 'fre', 'fme', 'hnr1', 'hei', 'hfg',
             'hen3', 'ifx', 'lin', 'mbg', 'mrk', 'mtx', 'muv2',
             'pah3', 'pum', 'qia', 'rwe', 'sap', 'srt3', 'sie',
             'shl', 'sy1', 'vow3', 'vna', 'zal']

test_symbols = ['ads', 'air', 'alv']


# Crawling web page with given URL
def get(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        return f'Error in URL Status Code: ERROR {res.status_code}'


def initialize_yf_tickers(companies: list):
    # Initialize yahooFinance Ticker for multiple companies and return it
    ticker = yf.Tickers(' '.join(companies))
    return ticker


def get_total_ESG_score(companies: list):
    # Get ticker for multiple companies
    ticker = initialize_yf_tickers(companies)

    # Iterate over every company and extract Total Sustainability Score
    total_esg_score = {}
    for company in companies:
        try:
            total_esg_score[f'{company}'] = ticker.tickers[str(company).upper()].sustainability.T['totalEsg']
            print("Producing record: {}\t{}".format(company, total_esg_score[f'{company}']))
        except AttributeError:
            total_esg_score[f'{company}'] = 'NaN'
            print(f"Error occured in fetching data from API for {company}. Continuing with next company.\n")
            continue

    return total_esg_score


def get_gross_profit_development(companies: list):
    ticker = initialize_yf_tickers(companies)
    total_profit_margins = {}
    for company in companies:
        try:
            print(f"Now executing: {company}")
            total_profit_margins[f'{company}'] = ticker.tickers[str(company).upper()].financials.T['Gross Profit']
        except Exception as e:
            total_profit_margins[f'{company}'] = 'NaN'
            print(f'For company: {company} following error occured: {e}')
    return total_profit_margins


def get_news_headlines():
    dax40_companies = ['adidas', 'bmw']
    # All news to be stored in a dictionary
    all_news = {}

    for company in dax40_companies:
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
        # print(f"+++ Finished Company: {company} +++\n")

        """
        # Top Headlines on website - status: tbd
        content = soup.find('span', attrs={"class": "teaser-headline"})
        # print(content.text)
        """

    return all_news

if __name__ == '__main__':
    # Next steps: Every headline as single message to KAFKA
    producer.produce(topic, json.dumps(get_news_headlines()), callback=delivery_report)
    producer.flush()
