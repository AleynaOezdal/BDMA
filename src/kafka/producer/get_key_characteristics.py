from bs4 import BeautifulSoup as bs
import json
from producersetup import (
    all_companies,
    send_msg,
    get,
    delivery_report,
    companies_url,
    kununu_companies,
    community_company,
    community_number,
    yfinance_symbols_dax_companies,
    all_cities,
)
import datetime as dt
import time
import pandas as pd
import yfinance as yf
from pytz import timezone


def get_key_characteristics(companies: list = all_companies):
    fmt = "%Y-%m-%d %H:%M:%S"
    for company in companies:
        comp_stock_prices = dict()
        try:
            base_url = f"https://www.finanzen.net/aktien/{company}-aktie"
            soup = bs(get(base_url), "html.parser")

            stock_price = {
                "price": soup.find("div", {"class": "row quotebox"})
                .find_all("div")[0]
                .text,
                "change": soup.find("div", {"class": "row quotebox"})
                .find_all("div")[2]
                .text,
                "open": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[5]
                .text.split()[0],
                "day_before": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[5]
                .text.split()[2],
                "highest": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[11]
                .text.split()[0],
                "lowest": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[11]
                .text.split()[2],
                "marketcap": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[9]
                .text,
                "time": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[3]
                .text.split()[1],
                "date": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[3]
                .text.split()[0],
            }

            comp_stock_prices[f"{company}"] = stock_price

            # Store company as key and stock price as value in a dict and transform it into JSON
            message = json.dumps(
                {
                    "company": company,
                    "key_characteristics": comp_stock_prices,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("key_characteristics", message)

        except Exception as e:
            # Send NaN-Value to ESG topic
            message = json.dumps(
                {
                    "company": company,
                    "key_characteristics": "NaN",
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("key_characteristics", message)

            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "key_characteristics",
                    "company": company,
                    "timestamp": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                    "error": repr(e),
                    "error_type": str(type(e)),
                }
            )
            send_msg("error", message)
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all key characteristics data to Kafka."


def start_producer(*args):
    get_key_characteristics()
