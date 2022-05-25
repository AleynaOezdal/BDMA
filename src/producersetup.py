import os
from dotenv import load_dotenv
from confluent_kafka import Producer
import yfinance as yf
import requests


load_dotenv()

p = Producer(
    {
        "bootstrap.servers": os.getenv("BOOTSTRAP.SERVERS.TEST"),
        "security.protocol": os.getenv("SECURITY.PROTOCOL.TEST"),
        "sasl.mechanisms": os.getenv("SASL.MECHANISMS.TEST"),
        "sasl.username": os.getenv("SASL.USERNAME.TEST"),
        "sasl.password": os.getenv("SASL.PASSWORD.TEST"),
    }
)


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    return "DONE."


all_companies = [
    "adidas",
    "airbus",
    "allianz",
    "basf",
    "bayer",
    "bmw",
    "brenntag",
    "continental",
    "covestro",
    "daimler_truck",
    "delivery_hero",
    "deutsche_bank",
    "deutsche_boerse",
    "deutsche_post",
    "deutsche_telekom",
    "eon",
    "fresenius",
    "fresenius_medical_care",
    "hannover_rueck",
    "heidelbergcement",
    "hellofresh",
    "henkel_vz",
    "infineon",
    "linde",
    "mercedes-benz",
    "porsche",
    "puma",
    "qiagen",
    "rwe",
    "sap",
    "sartorius_vz",
    "siemens",
    "siemens_healthineers",
    "symrise",
    "volkswagen",
    "vonovia",
    "zalando",
]

companies_url = [
    "adidas",
    "airbus",
    "allianz",
    "basf",
    "bayer",
    "bmw",
    "brenntag",
    "continental",
    "covestro",
    "daimler-truck",
    "deliveryhero",
    "deutsche-bank",
    "deutsche-boerse",
    "deutschepost",
    "telekom",
    "eon",
    "fresenius",
    "freseniusmedicalcare",
    "hannover-rueck",
    "heidelbergcement",
    "hellofresh",
    "henkel",
    "infineon",
    "linde-gas",
    "mercedes-benz",
    "porsche",
    "puma",
    "qiagen",
    "rwe",
    "sap",
    "sartorius",
    "siemens",
    "siemens-healthineers",
    "symrise",
    "volkswagen",
    "vonovia",
    "zalando",
]


# Source for DAX Symbols: https://de.wikipedia.org/wiki/DAX#Zusammensetzung
yfinance_symbols_dax_companies = [
    "ads",
    "air",
    "alv",
    "bas",
    "bayn",
    "bmw",
    "bnr",
    "con",
    "1cov",
    "dtg",
    "dher",
    "dbk",
    "db1",
    "dpw",
    "dte",
    "eoan",
    "fre",
    "fme",
    "hnr1",
    "hei",
    "hfg",
    "hen3",
    "ifx",
    "lin",
    "mbg",
    "mrk",
    "mtx",
    "muv2",
    "pah3",
    "pum",
    "qia",
    "rwe",
    "sap",
    "srt3",
    "sie",
    "shl",
    "sy1",
    "vow3",
    "vna",
    "zal",
]

test_symbols = ["ads", "air", "alv"]


def initialize_yf_tickers(companies: list):
    # Initialize yahooFinance Ticker for multiple companies and return it
    ticker = yf.Tickers(" ".join(companies))
    return ticker


# Crawling web page with given URL
# param :yahoo_finance: To crawl data from yahooFinance, we have to send a User-Agent Header, otherwise YF will block the request
def get(url, yahoo_finance=False):
    yahoo_finance_header = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    if yahoo_finance:
        res = requests.get(url, headers=yahoo_finance_header)
    else:
        res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        raise BaseException
