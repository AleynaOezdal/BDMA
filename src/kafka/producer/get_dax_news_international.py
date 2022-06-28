from bs4 import BeautifulSoup as bs
import json
from producersetup import send_msg
import datetime as dt
import time
import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
from pytz import timezone

fmt = "%Y-%m-%d %H:%M:%S"


def get_international_dax_news():
    try:
        dax = yf.Ticker("^GDAXI")
        for item in dax.news:
            message = json.dumps(
                {
                    "title": item["title"],
                    "publisher": item["publisher"],
                    "time_published": str(
                        dt.datetime.fromtimestamp(item["providerPublishTime"]).strftime(
                            fmt
                        )
                    ),
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                    "link": item["link"],
                }
            )
            send_msg("international_dax_news", message)

    except Exception as e:
        # Send Error-Object to error topic (DLQ)
        error_message = json.dumps(
            {
                "scraper": "international_dax_news",
                "timestamp": str(
                    dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                ),
                "error": repr(e),
            }
        )
        send_msg("error", error_message)
        print(f"FAILED. For DAX the following error occured: {type(e)}")

    return "Done. Produced all international news for DAX to Kafka."


def start_producer(*args):
    get_international_dax_news()
