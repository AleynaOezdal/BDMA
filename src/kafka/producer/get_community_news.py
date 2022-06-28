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


def get_community(companies: list = community_company, number: list = community_number):
    for company, numbers in zip(companies, number):
        try:
            base_url = f"https://www.boersennews.de/community/diskussion/{company}/{numbers}/#moreComments"
            soup = bs(get(base_url), "html.parser")
            count = 0
            found_community = soup.find(
                "div", {"class": "row row-cols-1 g-3 mt-0 justify-content-end"}
            ).find_all("div", {"class": "row g-3 mt-0 userPosting"})

            for chat in found_community:
                communities = {
                    "message": chat.find(
                        "div", {"class": "text-info text-break overflow-auto pe-3"}
                    )
                    .text.replace("  ", "")
                    .replace("\r", "")
                    .replace("\n", "")
                    .replace("\t", ""),
                    "timestamp": chat.find("small", {"class": "d-block text-truncate"})
                    .text.split()[2]
                    .replace("  ", "")
                    .replace("\r", "")
                    .replace("\n", "")
                    .replace("\t", ""),
                    "User": chat.find("small", {"class": "d-block text-truncate"})
                    .text.split()[0]
                    .replace("  ", "")
                    .replace("\r", "")
                    .replace("\n", "")
                    .replace("\t", ""),
                    "more info": base_url,
                }
                count += 1
                message = json.dumps(
                    {
                        "company": company,
                        "community_news": communities,
                        "time": str(
                            dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                        ),
                    }
                )
                send_msg("community_news", message)

        except Exception as e:
            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "community_news",
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

    return "Done. Produced all Community_news to Kafka."


def start_producer(*args):
    get_community()
