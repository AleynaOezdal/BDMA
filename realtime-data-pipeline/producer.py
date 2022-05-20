"""
: get stock price and news every minute
"""
from typing import Dict, Union
from confluent_kafka import Producer
import json
import requests
from bs4 import BeautifulSoup
from info import info, config
import yfinance as yf
from dotenv import load_dotenv
import os

# =============================================================================
# Scraper
# =============================================================================

# Crawling web page with given URL
def get(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        return f'Error in URL Status Code: ERROR {res.status_code}'

def get_stock_price(symbol):
    url = f"https://www.finanzen.net/aktien/{symbol}-aktie"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    stock_price = {
        "symbol": symbol,
        "price": soup.find("div", {"class": "row quotebox"}).find_all("div")[0].text,
        "change": soup.find("div", {"class": "row quotebox"}).find_all("div")[2].text,
        "open": soup.find("div", {"class": "box table-quotes"}).find_all("td")[5].text.split()[0],
        "day_before": soup.find("div", {"class": "box table-quotes"}).find_all("td")[5].text.split()[2],
        "highest": soup.find("div", {"class": "box table-quotes"}).find_all("td")[11].text.split()[0],
        "lowest": soup.find("div", {"class": "box table-quotes"}).find_all("td")[11].text.split()[2],
        "marketcap": soup.find("div", {"class": "box table-quotes"}).find_all("td")[9].text,
        "time": soup.find("div", {"class": "box table-quotes"}).find_all("td")[3].text.split()[1],
        "date": soup.find("div", {"class": "box table-quotes"}).find_all("td")[3].text.split()[0],
    }
    return json.dumps(stock_price)

def get_static_stock_price(symbol):
    ticker = yf.Ticker({symbol})
    stock_price = ticker.history(period="max")
    return stock_price

def get_holders(symbol):
    url = f"https://de.finance.yahoo.com/quote/{symbol}/holders?p={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

    x = soup.find("div", {"class":"W(100%) Mb(20px)"})

    results = {}
    for row in x.findAll('tr'):
        aux = row.findAll('td')
        results[aux[1].string] = aux[0].string

    return json.dumps(results)

def get_news(symbol):
    url = f"https://www.finanzen.net/aktien/{symbol}-aktie"
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        news_list = []
        news = soup.find("div", {"class": "col-sm-8 col-xs-12"}).find_all("div", {"class": "newsTeaser clearfix"})
        for new in news:
            newss = {
                "symbol": symbol,
                "headline": new.find("div", {"class": "newsTeaserText"}).find("a").text,
                "timestamp": new.find("div", {"class": "pull-left"}).text,
                "more_info": "https://www.finanzen.net/nachricht/aktien/" +
                             new.find("div", {"class": "newsTeaserText"}).a["href"],

            }
            news_list.append(newss)
        return json.dumps(news_list)
    else:
        print('  Failed: Cannot get {}\'s data at {}:{} '.format(symbol, r.status_code))
        value: Dict[str, Union[str, float]] = {"symbol": 'None',
                                               "headline": 'None',
                                               "timestamp": 0.,
                                               "more_info": "None", }

        return value

def get_mitarbeiter_reviews(symbol):
    url = f"https://www.kununu.com/de/{symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    review_list = []
    kununu_positive = soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"}).find("div", {"id":"summary-employees-like"}).find_all("div", {"class", "index__snippet__35vvF"})
    kununu_negative = soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"}).find("div", {"id":"summary-employees-dont-like"}).find_all("div", {"class", "index__snippet__35vvF"})
    kununu_suggestions = soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"}).find("div", {"id":"summary-employees-suggestions"}).find_all("div", {"class", "index__snippet__35vvF"})
    for i in kununu_positive:
        positive = {
            "positive" : i.find("q").text,
            "more info" : "https://www.kununu.com" + i.find("div", {"class": "index__snippetInfo__1OMUQ"}).a["href"]
        }
        review_list.append(positive)

    for x in kununu_negative:
        negative = {
            "negative" : x.find("q").text,
            "more info" : "https://www.kununu.com" + x.find("div", {"class": "index__snippetInfo__1OMUQ"}).a["href"]
        }
        review_list.append(negative)

    for x in kununu_suggestions:
        suggestions = {
            "suggestions" : x.find("q").text,
            "more info" : "https://www.kununu.com" + x.find("div", {"class": "index__snippetInfo__1OMUQ"}).a["href"]
        }
        review_list.append(suggestions)
    return json.dumps(review_list)

def get_Dax_news():
    url = "https://www.boerse.de/nachrichten/Dax-Aktien/DE0008469008"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    business = []
    news = soup.find("div", {"class":"newsKasten inhaltsKasten"}).find_all("div", {"class": "row row-bordered"})
    for i in news:
        business_news = {
            "headline": i.find("div", {"class": "col-xs-9 col-md-10"}).find("a").text.replace("  ", "").replace("\n", ""),
            "timestamp": i.find("div", {"class": "col-xs-3 col-md-2"}).text.replace("  ", "").replace("\n", ""),
            "more_info": i.find("div", {"class": "col-xs-9 col-md-10"}).a["href"],
        }
        business.append(business_news)
    return json.dumps(business)

def get_welt_news():
    url = "https://www.boerse.de/unternehmensnachrichten/welt/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    businesss = []
    news = soup.find("div", {"class": "newsKasten inhaltsKasten"}).find_all("div", {"class": "row row-bordered"})
    for i in news:
        business_news = {
            "headline": i.find("div", {"class": "col-xs-9 col-md-10"}).find("a").text.replace("  ", "").replace("\n",""),
            "timestamp": i.find("div", {"class": "col-xs-3 col-md-2"}).text.replace("  ", "").replace("\n", ""),
            "more_info": i.find("div", {"class": "col-xs-9 col-md-10"}).a["href"],
        }
        businesss.append(business_news)
    return json.dumps(businesss)

def get_forum():
    url = "https://www.boersennews.de/community/diskussion/adidas/109/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    commi = []
    com = soup.find("div", {"class":"row row-cols-1 g-3 mt-0 justify-content-end"}).find_all("div", {"class":"row g-3 mt-0 userPosting"})
    for i in com:
        community= {
            "message": i.find("div", {"class":"text-info text-break overflow-auto"}).text.replace("  ", "").replace("\r", "").replace("\n", "").replace("\t", ""),
            "timestamp" : i.find("small", {"class":"d-block text-truncate"}).text.split()[2].replace("  ", "").replace("\r", "").replace("\n", "").replace("\t", ""),
            "User": i.find("small", {"class": "d-block text-truncate"}).text.split()[0].replace("  ", "").replace("\r", "").replace("\n", "").replace("\t", ""),
            "more info": url
        }
        commi.append(community)
    return json.dumps(commi)


def get_kunden(symbol):
    url = f"https://de.trustpilot.com/review/{symbol}"
    r = requests.get(url)
    soup= BeautifulSoup(r.text, "html.parser")
    trusti = []
    custom = soup.find("section", {"class":"styles_reviewsContainer__3_GQw"}).find_all("section", {"class":"styles_reviewContentwrapper__zH_9M"})
    print(custom)
    for i in custom:
        trustpilot= {
            "title": i.find("a").text,
            "review": i.find("div", {"class":"styles_reviewContent__0Q2Tg"}).contents[-1].text,
            "time": i.find("div", {"class":"typography_typography__QgicV typography_bodysmall__irytL typography_color-gray-6__TogX2 typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 styles_datesWrapper__RCEKH"}).text,
            "more info": url + i.a["href"]
        }
        trusti.append(trustpilot)
    return json.dumps(trusti)





#
# #test yahoo Scraper
# def get_yahoo_data():
#     url = "https://finance.yahoo.com/quote/ADS.DE/key-statistics?p=ADS.DE"
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
#     }
#
#     soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
#
#     for t in soup.select("table"):
#         for tr in t.select("tr:has(td)"):
#             for sup in tr.select("sup"):
#                 sup.extract()
#             tds = [td.get_text(strip=True) for td in tr.select("td")]
#             if len(tds) == 2:
#                 print("{:<50} {}".format(*tds))
#
# def get_kpi():
#     url = "https://finance.yahoo.com/quote/ADS.DE/financials?p=ADS.DE"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
#     }
#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.text, "html.parser")
#     kpi = soup.find("div", {"class":"D(tbrg)"}).select("span")[15].text
#
#     print(kpi)


#Kafka Producer

load_dotenv()

p = Producer({
    'bootstrap.servers': os.getenv("BOOTSTRAP.SERVERS"),
    'security.protocol': os.getenv("SECURITY.PROTOCOL"),
    'sasl.mechanisms': os.getenv("SASL.MECHANISMS"),
    'sasl.username': os.getenv("SASL.USERNAME"),
    'sasl.password': os.getenv("SASL.PASSWORD")
 })

topic = 'test'


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))



if __name__ == "__main__":
    print(get_welt_news())
    # for i in info.dax_unternehmen:
        # p.produce(topic, json.dumps(get_stock_price(i)), callback= delivery_report)
        # p.flush()












