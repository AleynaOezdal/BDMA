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
from dateutil.relativedelta import relativedelta
from pytz import timezone

fmt = "%Y-%m-%d %H:%M:%S"
timestamp = dt.datetime.now() - dt.timedelta(minutes=15)
timestamp_end = timestamp
timestamp_start = timestamp - dt.timedelta(hours=1)
time_end = dt.datetime.strptime(timestamp_end.strftime(fmt), "%Y-%m-%d %H:%M:%S")
time_start = dt.datetime.strptime(timestamp_start.strftime(fmt), "%Y-%m-%d %H:%M:%S")


def get_stock_price_onehour(
    companies: list = yfinance_symbols_dax_companies + ["^GDAXI"],
):
    print(timestamp)
    for company in companies:
        try:
            if company == "^GDAXI":
                suffix = ""
            else:
                suffix = ".DE"
            record_value = yf.download(
                f"{company.upper()+suffix}",
                start=time_start,
                end=time_end,
                interval="1m",
                group_by="ticker",
            ).to_json()

            # Store company as key and stock history as value in a dict and transform it into JSON
            # Note: record_value is a DataFrame to json. In the frontend, we'll need to transform it back into a DF.
            # Steps: res = json.loads(value), then result = pd.json_normalize(res)
            message = json.dumps(
                {
                    "company": company,
                    "stock_price_onehour": record_value,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("stock_price_lasthour", message)
            # print(message)

        except Exception as e:
            # Send NaN-Value to ESG topic
            message = json.dumps(
                {
                    "company": company,
                    "stock_price_onehour": "NaN",
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("stock_price_lasthour", message)
            # print(message)

            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "stock_price_last_hour",
                    "company": company,
                    "timestamp": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                    "error": repr(e),
                    "error_type": str(type(e)),
                }
            )
            send_msg("error", message)
            # print(error_message)
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all stock data to Kafka."


def start_producer(*args):
    get_stock_price_onehour()
