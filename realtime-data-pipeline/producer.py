"""
: get stock price and news every minute
"""

import json
import requests
from bs4 import BeautifulSoup
from info import info, config

# =============================================================================
# Scraper + Producer
# =============================================================================


def get_stock_price(symbol):
    url = f"https://www.finanzen.net/aktien/{symbol}-aktie"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    stock_price = {
        "symbol": symbol,
        "price": soup.find("div", {"class": "row quotebox"}).find_all("div")[0].text,
        "change": soup.find("div", {"class": "row quotebox"}).find_all("div")[2].text,
    }
    return stock_price

# preisliste = []
# for i in info.dax_unternehmen:
#     preisliste.append(get_stock_price(i))
#     print(preisliste)

def get_news(symbol):
    url = f"https://www.finanzen.net/aktien/{symbol}-aktie"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    news = {
        "symbol": symbol,
        "headline": soup.find("table", {"class": "table news-list"}).find_all("a").text.replace("  ", "").strip(),
        "time": soup.find("table", {"class": "table news-list"}).find_all("span").text.replace("  ", "").strip(),
        "more_info": soup.find("table", {"class": "table news-list"}).find_all("a")["href"].strip(),
    }
    return news

