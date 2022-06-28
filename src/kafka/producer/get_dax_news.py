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
)
import datetime as dt
import time
import pandas as pd
import yfinance as yf
from pytz import timezone

fmt = "%Y-%m-%d %H:%M:%S"


def get_dax_news():
    try:
        base_url = "https://www.finanzen.net/index/dax/marktberichte"
        soup = bs(get(base_url), "html.parser")
        found_news = (
            soup.find("div", {"id": "general-news-table"})
            .find("table", {"class": "table"})
            .find_all("tr")
        )
        count = 0
        for headline in found_news:
            headline_news = {
                "headline": headline.find("a").text,
                "timestamp": headline.find("td", {"class": "col-date"})
                .text.replace("  ", "")
                .replace("\n", "")
                .replace("\r", "")
                .replace("\t", ""),
                "more_info": base_url,
            }
            count += 1
            # Generate unique key with company and iterating count
            # Store headline as value for specific key
            # Store company as key and headline as value in a dict and transform it into JSON

            message = json.dumps(
                {
                    "news": headline_news,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("dax_news", message)

    except Exception as e:
        dax_news = "NaN"
        # Send NaN-Value to weather topic
        message = json.dumps(
            {
                "news": dax_news,
                "time": str(dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)),
            }
        )
        send_msg("dax_news", message)

        # Send Error-Object to error topic (DLQ)
        error_message = json.dumps(
            {
                "scraper": "dax_news",
                "timestamp": str(
                    dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                ),
                "error": repr(e),
                "error_type": type(e),
            }
        )
        send_msg("error", error_message)
        print(f"FAILED. For Dax News the following error occured: {type(e)}")

    return "Done. Produced all Dax News to Kafka."


def start_producer(*args):
    get_dax_news()
