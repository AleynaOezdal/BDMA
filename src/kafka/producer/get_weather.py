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


def get_weather(cities: list = all_cities):
    fmt = "%Y-%m-%d %H:%M:%S"
    for city in cities:

        try:
            base_url = f"https://www.wetteronline.de/wetter/{city}"
            soup = bs(get(base_url), "html.parser")
            weather = soup.find("div", {"id": "p_city_weather"})
            weather_temp = {
                "Ort": weather.find("h1", {"id": "nowcast-card-headline"}).text[7:],
                "Temperatur": weather.find("div", {"class": "forecast visible"})
                .find("div", {"class": "big temperature"})
                .text.replace("  ", "")
                .replace("\n", ""),
            }

            # Store extracted data in a dict and transform it to JSON
            message = json.dumps(
                {
                    "city": city,
                    "temp": weather_temp,
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("weather", message)

        # Error Handling Strategy: Dead-Letter-Queues (DLQ)
        except Exception as e:
            weather_temp = "NaN"
            # Send NaN-Value to weather topic
            message = json.dumps(
                {
                    "city": city,
                    "temp": "NaN",
                    "time": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                }
            )
            send_msg("weather", message)

            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "weather",
                    "city": city,
                    "timestamp": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                    "error": repr(e),
                    "error_type": type(e),
                }
            )
            send_msg("error", error_message)
            print(f"FAILED. For {city} the following error occured: {type(e)}")

    return "Done. Produced all weather data to Kafka."


def start_producer(*args):
    get_weather()
