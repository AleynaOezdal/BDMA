import pprint

import pymongo
import os
from dotenv import load_dotenv
import certifi
from bs4 import BeautifulSoup as bs
import requests
import yfinance as yf

load_dotenv()

client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

"""
Adding now news data
"""
news_db = client['news']
headline_collection = news_db['corporate_news']

def get(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        return f'Error in URL Status Code: ERROR {res.status_code}'

def get_news_headlines():
    dax40_companies = ['apple']
    # All news to be stored in a dictionary
    all_news = []
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
            company_news_dict = dict()
            company_news_dict[f"{company}_{count}"] = headline.text
            count += 1
            all_news.append(company_news_dict)
        # print(f"+++ Finished Company: {company} +++\n")
    return all_news

def insert_samplenews_into_mongodb():
    news_dict = get_news_headlines()
    for headline in news_dict:
        for k, v in headline.items():
            post = {"_id": k, "headline": v}
            headline_collection.insert_one(post)

"""
Adding now stock data
"""

stock_db = client['stocks']
chart_collection = news_db['chart']

def get_chart_data():
    apple = yf.download('AAPL', start="2022-05-17").to_dict()
    pprint.pprint(apple)


if __name__ == '__main__':
    insert_samplenews_into_mongodb()
    #get_chart_data()