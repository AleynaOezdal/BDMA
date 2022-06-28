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

fmt = "%Y-%m-%d %H:%M:%S"


def get_news(companies: list = all_companies):

    for company in companies:

        try:
            base_url = f"https://www.finanzen.net/aktien/{company}-aktie"
            soup = bs(get(base_url), "html.parser")
            found_news = soup.find("div", {"class": "col-sm-8 col-xs-12"}).find_all(
                "div", {"class": "newsTeaser clearfix"}
            )
            count = 0
            for headline in found_news:
                headline_news = {
                    "headline": headline.find("div", {"class": "newsTeaserText"})
                    .find("a")
                    .text,
                    "timestamp": headline.find("div", {"class": "pull-left"}).text,
                    "more_info": "https://www.finanzen.net/nachricht/aktien/"
                    + headline.find("div", {"class": "newsTeaserText"}).a["href"],
                }
                count += 1
                # Generate unique key with company and iterating count
                # Store headline as value for specific key
                # Store company as key and headline as value in a dict and transform it into JSON

                message = json.dumps(
                    {
                        "company": company,
                        "news": headline_news,
                        "time": str(
                            dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                        ),
                    }
                )
                send_msg("company_news", message)

        except Exception as e:
            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "company_news",
                    "company": company,
                    "timestamp": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                    "error": repr(e),
                    "error_type": type(e),
                }
            )
            send_msg("error", error_message)
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all News to Kafka."


def start_producer(*args):
    get_news()
