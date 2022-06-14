from bs4 import BeautifulSoup as bs
import json
from producersetup import (
    all_companies,
    delivery_report,
    get,
    p,
    companies_url,
    kununu_companies,
    community_company,
    community_number,
    yfinance_symbols_dax_companies,
)
import datetime as dt
import time
from dateutil.relativedelta import relativedelta
import pandas as pd
import yfinance as yf


def get_stock_price_last_hour(
    companies: list = yfinance_symbols_dax_companies + ["^GDAXI"],
):
    for company in companies:
        try:
            suffix = ".DE"
            if company == "^GDAXI":
                suffix = ""
            record_value = yf.download(
                f"{company.upper()+suffix}",
                start=dt.datetime.now() - relativedelta(hours=1),
                end=dt.datetime.now(),
                interval="1m",
                group_by="ticker",
            ).to_json()

            # Store company as key and stock history as value in a dict and transform it into JSON
            # Note: record_value is a DataFrame to json. In the frontend, we'll need to transform it back into a DF.
            # Steps: res = json.loads(value), then result = pd.json_normalize(res)
            p.produce(
                "stock_price_onehour",
                json.dumps(
                    {
                        "company": company,
                        "stock_price_onehour": record_value,
                        "time": str(dt.datetime.now()),
                    }
                ),
                callback=delivery_report,
            )
            p.flush()

        except Exception as e:
            # Send NaN-Value to stock_data_one_hour topic
            message = json.dumps(
                {
                    "company": company,
                    "stock_price_onehour": "NaN",
                    "time": str(dt.datetime.now()),
                }
            )
            p.produce("stock_price_onehour", message, callback=delivery_report)
            p.flush()

            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "stock_price_onehour",
                    "company": company,
                    "timestamp": str(dt.datetime.now()),
                    "error": repr(e),
                    "error_type": str(type(e)),
                }
            )
            p.produce("error", error_message, callback=delivery_report)
            p.flush()
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all stock data to Kafka."


def get_key_characteristics(companies: list = all_companies):

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
            p.produce(
                "key_characteristics",
                json.dumps(
                    {
                        "company": company,
                        "key_characteristics": comp_stock_prices,
                        "time": str(dt.datetime.now()),
                    }
                ),
                callback=delivery_report,
            )
            p.flush()

        except Exception as e:
            # Send NaN-Value to ESG topic
            message = json.dumps(
                {
                    "company": company,
                    "key_characteristics": "NaN",
                    "time": str(dt.datetime.now()),
                }
            )
            p.produce("key_characteristics", message, callback=delivery_report)
            p.flush()

            # Send Error-Object to error topic (DLQ)
            error_message = json.dumps(
                {
                    "scraper": "key_characteristics",
                    "company": company,
                    "timestamp": str(dt.datetime.now()),
                    "error": repr(e),
                    "error_type": str(type(e)),
                }
            )
            p.produce("error", error_message, callback=delivery_report)
            p.flush()
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all Stock Prices to Kafka."


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
                p.produce(
                    "company_news",
                    json.dumps(
                        {
                            "_id": f"{company}_{count}",
                            "news": headline_news,
                            "time": str(dt.datetime.now()),
                        }
                    ),
                    callback=delivery_report,
                )
                p.flush()

        except Exception as e:
            # Because there a lots of news for each DAX company, we don't produce a failed news item to Kafka
            print(f"FAILED. For {company} the following error occured: {type(e)}")
            continue

    return "Done. Produced all News to Kafka."


def get_worker_review(companies: list = kununu_companies):

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
                    "_id": f"{company}_{count}",
                    "positive_reviews": positive,
                    "time": str(dt.datetime.now()),
                }
                count += 1

                p.produce("Reviews", json.dumps(post), callback=delivery_report)
                p.flush()

            for review in kununu_negative:
                negative = {
                    "negative": review.find("q").text,
                    "more info": "https://www.kununu.com"
                    + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a[
                        "href"
                    ],
                }
                post = {
                    "_id": f"{company}_{count}",
                    "negative_reviews": negative,
                    "time": str(dt.datetime.now()),
                }
                count += 1

                p.produce("Reviews", json.dumps(post), callback=delivery_report)
                p.flush()

            for review in kununu_suggestions:
                suggestions = {
                    "suggestions": review.find("q").text,
                    "more info": "https://www.kununu.com"
                    + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a[
                        "href"
                    ],
                }
                post = {
                    "_id": f"{company}_{count}",
                    "suggestions": suggestions,
                    "time": str(dt.datetime.now()),
                }
                count += 1

                p.produce("Reviews", json.dumps(post), callback=delivery_report)
                p.flush()

        except BaseException as e:
            print(f"FAILED. For {company} the following error occured: {type(e)}")
            continue

    return "Done. Produced all Reviews to Kafka."


def get_world_news():

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
                    p.produce(
                        "world_news",
                        json.dumps(
                            {
                                "_id": f"Welt-News_{count}",
                                "headline": headline_news,
                                "time": str(dt.datetime.now()),
                            }
                        ),
                        callback=delivery_report,
                    )
                    p.flush()
            except Exception as e:
                # Since general news are existing in high quantity, we won't produce here anything to Kafka.
                print(f"FAILED. For Welt-News the following error occured: {type(e)}")
                continue

    except Exception as e:
        # Since general news are existing in high quantity, we won't produce here anything to Kafka.
        print(f"FAILED. For Welt-News the following error occured: {type(e)}")

    return "Done. Produced all World-news to Kafka."


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

                p.produce(
                    "Community_news",
                    json.dumps(
                        {
                            "_id": f"{company}_{count}",
                            "community_news": communities,
                            "time": str(dt.datetime.now()),
                        }
                    ),
                    callback=delivery_report,
                )
                p.flush()

        except Exception as e:
            print(f"FAILED. For {company} the following error occured: {type(e)}")
            continue

    return "Done. Produced all Community_news to Kafka."


def get_customer_experience(companies: list = companies_url):
    # URL Handling: Not every company's website ends on .com, so we have to list which do and use a different slug for those who not
    dotcom_companies = [
        "airbus",
        "basf",
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
                p.produce(
                    "Customer_experience",
                    json.dumps(
                        {
                            "_id": f"{company}_{count}",
                            "customer_exp": cus_exp,
                            "time": str(dt.datetime.now()),
                        }
                    ),
                    callback=delivery_report,
                )
                p.flush()

        except BaseException as e:
            p.produce(
                "Customer_experience",
                json.dumps(
                    {
                        str(company): "No reviews available",
                        "time": str(dt.datetime.now()),
                    }
                ),
                callback=delivery_report,
            )
            p.flush()
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return "Done. Produced all Customer_experience to Kafka."


if __name__ == "__main__":
    # Next steps: Every headline as single message to KAFKA
    # WARN: Only start if kafka cluster is set up!

    # get_actual_stock_price()
    """
    print("Now: News for all DAX Companies ...")
    get_news()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Employees' Reviews for all DAX Companies ...")
    get_worker_review()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Global News for all DAX Companies ...")
    get_world_news()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Community Chats for all DAX Companies ...")
    get_community()

    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Customer Experiences from Trustpilot for all DAX Companies ...")
    get_customer_experience()
    print("Completed.")"""
    # pass

    get_stock_price_last_hour()
