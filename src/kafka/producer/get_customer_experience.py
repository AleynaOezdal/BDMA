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


def get_customer_experience(companies: list = companies_url):
    # URL Handling: Not every company's website ends on .com, so we have to list which do and use a different slug for those who not
    dotcom_companies = [
        "airbus",
        "basf",
        "bayer",
        "beiersdorf",
        "brenntag",
        "deutsche-boerse",
        "fresenius",
        "freseniusmedicalcare",
        "infineon",
        "merckgroup",
        "munichre",
        "porsche",
        "puma",
        "qiagen",
        "rwe",
        "sap",
        "sartorius",
        "siemens",
        "siemens-healthineers",
        "symrise",
    ]

    for company in companies:

        if company not in dotcom_companies:
            base_url = (
                f"https://de.trustpilot.com/review/www.{company.replace('_','')}.de"
            )
        else:
            base_url = (
                f"https://de.trustpilot.com/review/www.{company.replace('_','')}.com"
            )

        try:
            soup = bs(get(base_url), "html.parser")
            count = 0
            found_cus_exp = soup.find(
                "section", {"class": "styles_reviewsContainer__3_GQw"}
            ).find_all("section", {"class": "styles_reviewContentwrapper__zH_9M"})

            for experience in found_cus_exp:
                try:
                    cus_exp = {
                        "title": experience.find("a").text,
                        "review": experience.find(
                            "div", {"class": "styles_reviewContent__0Q2Tg"}
                        )
                        .contents[-1]
                        .text,
                        "time": experience.find(
                            "div",
                            {
                                "class": "typography_typography__QgicV typography_bodysmall__irytL typography_color-gray-6__TogX2 typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 styles_datesWrapper__RCEKH"
                            },
                        ).text,
                        "more info": base_url + experience.a["href"],
                    }
                    count += 1

                    message = json.dumps(
                        {
                            "company": company,
                            "customer_exp": cus_exp,
                            "time": str(
                                dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                            ),
                        }
                    )
                    send_msg("customer_experience", message)
                except Exception as e:

                    error_message = json.dumps(
                        {
                            "scraper": "customer_experience",
                            "company": company,
                            "timestamp": str(
                                dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                            ),
                            "error": repr(e),
                        }
                    )
                    send_msg("error", error_message)

        except Exception as e:
            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "customer_experience",
                    "company": company,
                    "timestamp": str(
                        dt.datetime.now(timezone("Europe/Berlin")).strftime(fmt)
                    ),
                    "error": repr(e),
                }
            )
            send_msg("error", error_message)
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all Customer_experience to Kafka."


def start_producer(*args):
    get_customer_experience()
