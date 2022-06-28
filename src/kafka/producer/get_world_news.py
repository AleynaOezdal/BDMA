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


def get_world_news():
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        base_url = "https://www.boerse.de/unternehmensnachrichten/welt/"
        soup = bs(get(base_url), "html.parser")
        found_news = soup.find("div", {"class": "newsKasten inhaltsKasten"}).find_all(
            "div", {"class": "row row-bordered"}
        )
        count = 0

        for headline in found_news:
            try:
                if headline.find("div", {"class": "col-xs-9 col-md-10"}) == EOFError:
                    continue
                else:
                    headline_news = {
                        "headline": headline.find(
                            "div", {"class": "col-xs-9 col-md-10"}
                        )
                        .find("a")
                        .text.replace("  ", "")
                        .replace("\n", ""),
                        "timestamp": headline.find(
                            "div", {"class": "col-xs-3 col-md-2"}
                        )
                        .text.replace("  ", "")
                        .replace("\n", ""),
                        "more_info": headline.find(
                            "div", {"class": "col-xs-9 col-md-10"}
                        ).a["href"],
                    }
                    count += 1
                    # Store as key and news as value in a dict
                    # Transform dict into JSON and produce it to Kafka

                    message = json.dumps(
                        {
                            "headline": headline_news,
                            "time": str(
                                dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                            ),
                        }
                    )
                    send_msg("world_news", message)

            except Exception as e:
                # Send NaN-Value to weather topic
                message = json.dumps(
                    {
                        "headline": "NaN",
                        "time": str(
                            dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                        ),
                    }
                )
                send_msg("world_news", message)

                # Send Error-Object to error topic (DLQ)
                error_message = json.dumps(
                    {
                        "scraper": "world_news",
                        "timestamp": str(
                            dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                        ),
                        "error": repr(e),
                        "error_type": str(type(e)),
                    }
                )
                send_msg("error", error_message)
                print(f"FAILED. In World News the following error occured: {type(e)}")

    except Exception as e:
        # Since general news are existing in high quantity, we won't produce here anything to Kafka.
        message = json.dumps(
            {
                "found_news": "NaN",
                "time": str(dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)),
            }
        )
        send_msg("world_news", message)

        # Send Error-Object to error topic (DLQ)
        error_message = json.dumps(
            {
                "scraper": "world_news",
                "timestamp": str(
                    dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                ),
                "error": repr(e),
                "error_type": str(type(e)),
            }
        )
        send_msg("error", error_message)
        print(f"FAILED. For Welt-News the following error occured: {type(e)}")

    return "Done. Produced all World-news to Kafka."


def start_producer(*args):
    get_world_news()
