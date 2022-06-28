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


def get_worker_review(companies: list = kununu_companies):
    fmt = "%Y-%m-%d %H:%M:%S"
    for company in companies:
        try:
            base_url = f"https://www.kununu.com/de/{company}"
            soup = bs(get(base_url), "html.parser")
            kununu_positive = (
                soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"})
                .find("div", {"id": "summary-employees-like"})
                .find_all("div", {"class", "index__snippet__35vvF"})
            )
            kununu_negative = (
                soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"})
                .find("div", {"id": "summary-employees-dont-like"})
                .find_all("div", {"class", "index__snippet__35vvF"})
            )
            kununu_suggestions = (
                soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"})
                .find("div", {"id": "summary-employees-suggestions"})
                .find_all("div", {"class", "index__snippet__35vvF"})
            )

            count = 0
            for review in kununu_positive:
                positive = {
                    "positive": review.find("q").text,
                    "more info": "https://www.kununu.com"
                    + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a[
                        "href"
                    ],
                }
                post = {
                    "company": company,
                    "positive_reviews": positive,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
                count += 1

                message = json.dumps(post)
                send_msg("worker_reviews", message)

            for review in kununu_negative:
                negative = {
                    "negative": review.find("q").text,
                    "more info": "https://www.kununu.com"
                    + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a[
                        "href"
                    ],
                }
                post = {
                    "company": company,
                    "negative_reviews": negative,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
                count += 1

                message = json.dumps(post)
                send_msg("worker_reviews", message)

            for review in kununu_suggestions:
                suggestions = {
                    "suggestions": review.find("q").text,
                    "more info": "https://www.kununu.com"
                    + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a[
                        "href"
                    ],
                }
                post = {
                    "company": company,
                    "suggestions": suggestions,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
                count += 1

                message = json.dumps(post)
                send_msg("worker_reviews", message)

        except Exception as e:
            worker_reviews = "NaN"
            # Send NaN-Value to weather topic
            message = json.dumps(
                {
                    "company": company,
                    "worker_reviews": worker_reviews,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("worker_reviews", message)

            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "worker_reviews",
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

    return "Done. Produced all Reviews to Kafka."


def start_producer(*args):
    get_worker_review()
