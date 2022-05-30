"""
Here we will extract data from the internet which won't change in June 2022
"""
from re import M
import time
import datetime as dt
import json
from bs4 import BeautifulSoup as bs
import yfinance as yf
from producersetup import (
    p,
    get,
    yfinance_symbols_dax_companies,
    delivery_report,
    all_companies,
    m_corps,
    initialize_yf_tickers,
)


def get_industry_and_competitors():
    try:
        base_url = "https://www.boerse.de/beste-schlechteste/Dax-Aktien/DE0008469008"
        soup = bs(get(url=base_url), "html.parser")

        industries = soup.find_all("tr", attrs={"class": "branche row-bordered"})
        all_industries = [
            str(industry.find("td").text.strip()) for industry in industries
        ]

        companies = soup.find_all("tr", attrs={"class": "aktie row-bordered"})
        allco = [str(company.find("a").text.strip()) for company in companies]

        dax40_distribution = [
            {all_industries[0]: allco[:6]},
            {all_industries[1]: allco[6:15]},
            {all_industries[2]: allco[15:19]},
            {all_industries[3]: allco[19:32]},
            {all_industries[4]: allco[32:34]},
            {all_industries[5]: allco[34:37]},
            {all_industries[6]: allco[37:39]},
            {all_industries[7]: allco[39:]},
        ]

        for pair in dax40_distribution:
            for k, v in pair.items():
                p.produce(
                    "dax40_distribution",
                    json.dumps(
                        {
                            "_id": k,
                            "corporates_in_industry": v,
                            "time": str(dt.datetime.now()),
                        }
                    ),
                    callback=delivery_report,
                )
                p.flush()

    except Exception as e:
        print(f"FAILED. The following error occured: {type(e)}\n{e}")

    return "Done. Produced all DAX industries to Kafka."


def get_description(companies: list = all_companies):

    for company in companies:
        try:
            base_url = f"https://www.finanzen.net/unternehmensprofil/{company}"
            soup = bs(get(base_url), "html.parser")
            description = soup.find("div", {"class": "col-sm-8"}).contents[1]
            description = str(description).split("</div>")[1]

        except Exception as e:
            description = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        p.produce(
            "company_description",
            json.dumps(
                {
                    "_id": company,
                    "company_description": description,
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()

    return "Done. Produced all company_description to Kafka."


def get_WKN_and_ISIN(companies: list = all_companies):
    # Scrape finanzen.net for each company for WKN/ ISIN
    for company in companies:
        try:
            base_url = f"https://www.finanzen.net/aktien/{company}-aktie"
            soup = bs(get(base_url), "html.parser")
            identification_numbers = soup.find(
                "span", attrs={"class": "instrument-id"}
            ).text

        except Exception as e:
            identification_numbers = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and WKN/ISIN as value in a dict and transform it into JSON
        p.produce(
            "wkns_and_isins",
            json.dumps(
                {
                    "_id": company,
                    "wkns_and_isins": identification_numbers,
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()

    return "Done. Produced all WKNs and ISINs to Kafka."


def get_holders(companies: list = yfinance_symbols_dax_companies):
    for company in companies:
        holders = dict()
        try:
            suffix = ".DE"
            base_url = f"https://de.finance.yahoo.com/quote/{company.upper()+suffix}/holders?p={company.upper()+suffix}"
            soup = bs(get(base_url, yahoo_finance=True), "html.parser")

            found_holders = soup.find("div", {"class": "W(100%) Mb(20px)"})
            for row in found_holders.findAll("tr"):
                holder = row.findAll("td")
                holders[holder[1].string] = holder[0].string

        except Exception as e:
            holders = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and major holders of the company as value in a dict and transform it into JSON
        p.produce(
            "holders",
            json.dumps(
                {"_id": company, "holders": holders, "time": str(dt.datetime.now())}
            ),
            callback=delivery_report,
        )
        p.flush()
    return "Done. Produced all holders to Kafka."


# TBD: to be discussed in which format to send to kafka and in which type of database to store
def get_history_stock_price(companies: list = yfinance_symbols_dax_companies):
    for company in companies:
        try:
            suffix = ".DE"
            record_value = yf.download(
                f"{company.upper()+suffix}",
                start="2022-05-01",
                end="2022-05-21",
                interval="1d",
                group_by="ticker",
            ).to_json()

        except Exception as e:
            record_value = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and stock history as value in a dict and transform it into JSON
        # Note: record_value is a DataFrame to json. In the frontend, we'll need to transform it back into a DF.
        # Steps: res = json.loads(value), then result = pd.json_normalize(res)
        p.produce(
            "history_stock_price",
            json.dumps(
                {
                    "_id": company,
                    "history_stock_price": record_value,
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()

    return "Done. Produced all stock data to Kafka."


def get_ESG_score(companies: list = yfinance_symbols_dax_companies):
    # Iterate over every company and extract ESG Score
    for company in companies:
        try:
            suffix = ".DE"
            company_ticker = yf.Ticker(f"{company.upper()+suffix}")
            # To create the value in a suitable way, we have to transpose the sustainability data frame
            # in order to extract the Total ESG Score.
            record_value = company_ticker.sustainability.T["totalEsg"]["Value"]

        except Exception as e:
            record_value = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        p.produce(
            "esg",
            json.dumps(
                {
                    "_id": company,
                    "esg_score": record_value,
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()
        time.sleep(7)

    return "Done. Produced all ESGs to Kafka."


# We can extract every KPI for each DAX40 company by changing the argument of the get_financial_KPI function.
# Instead of implementing five individual functions with the same structure, we only pass the KPI as an argument.
financial_KPIs = [
    "Gross Profit",
    "Ebit",
    "Total Revenue",
    "Net Income",
    "Total Operating Expenses",
]

# Convert dictionary keys from given data type to string
def convert_timestamps_keys_to_str(d: dict):
    return {str(k): v for k, v in d.items()}


def get_kpi_topic(kpi: str):
    # Because Confluent Kafka doesn't allow blank spaces within a topic name,
    # we replace the blank space in the kpi's name with an underscore.
    return kpi.replace(" ", "_")


def get_financial_KPI(
    kpi: str, companies: list = yfinance_symbols_dax_companies, yearly_basis=True
):
    # Iterate over every company and extract gross profit development
    for company in companies:
        # Due to some performance issues
        time.sleep(15)
        try:
            # The Suffix is required for finance.yahoo.com, otherwise it won't recognize the symbol
            suffix = ".DE"
            company_ticker = yf.Ticker(f"{company.upper()+suffix}")
            # To create the value in a suitable way, we have to transpose the kpi data frame
            # in order to extract the kpi and its value over the years (since 2019).
            if yearly_basis:
                record_value = company_ticker.financials.T[kpi].to_dict()
            else:
                record_value = company_ticker.quarterly_financials.T[kpi].to_dict()

        except Exception as e:
            record_value = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Because yfinance returns a DataFrame with timestamps as keys, we have to convert them into a string
        # since Timestamps won't work as json key
        record_value = convert_timestamps_keys_to_str(record_value)

        p.produce(
            get_kpi_topic(kpi),
            json.dumps(
                {"_id": company, f"{kpi}": record_value, "time": str(dt.datetime.now())}
            ),
            callback=delivery_report,
        )
        p.flush()

    return f"Done. Produced {financial_KPIs} for all DAX40 companies to Kafka."


def get_DAX_history_stock_price_til_today(
    end=str(dt.datetime.today()).split(" ")[0], *args
):
    dax_stock_data = yf.download("^GDAXI", start="2015-01-01", end=end, *args)
    for stock_day in range(len(dax_stock_data)):
        p.produce(
            "dax_history_stock_data",
            json.dumps(
                {
                    "_id": f"DAX40_{stock_day}",
                    "stock_history_til_date": dax_stock_data.iloc[stock_day].to_json(),
                    "stock_date": str(dax_stock_data.iloc[stock_day].name).split(" ")[
                        0
                    ],
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()
    return "DONE. DAX Stock Evolution is produced successfully."


def get_dividends(companies: list = yfinance_symbols_dax_companies):
    for company in companies:
        suffix = ".DE"
        record_value = yf.Ticker(company.upper() + suffix).dividends.to_json()
        p.produce(
            "dividends",
            json.dumps(
                {
                    "_id": company,
                    "dividends": record_value,
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()
        time.sleep(5)
    return "DONE."


if __name__ == "__main__":
    # Test if all KPIs are extractable
    print("Now: WKNs and ISINs for all DAX Companies ...")

    time.sleep(5)
    get_WKN_and_ISIN()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: ESG Score for all DAX Companies ...")
    get_ESG_score()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: All finance KPIs for all DAX Companies ...")
    for kpi in financial_KPIs:
        print(f"Now extracting {kpi}. Wait ...")
        print(f"Listing now all DAX40 companies with all {kpi.upper()} values.\n")
        get_financial_KPI(kpi=kpi, yearly_basis=True)
        print("Done. Waiting for 120 seconds.")
        time.sleep(120)

    print("Now: Major Holders for all DAX Companies ...")
    get_holders()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Yearly Dividends for all DAX Companies ...")
    get_dividends()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: History DAX price for all DAX Companies ...")
    get_DAX_history_stock_price_til_today()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Description for all DAX Companies ...")
    get_description()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    print("Now: Industry and Competitors for all DAX Companies ...")
    get_industry_and_competitors()
    print("Done. Waiting for 5 seconds.")
    time.sleep(5)

    # tbd: get_history_stock_price()
