"""
Here we will extract data from the internet which won't change in June 2022
"""
import time
import json
from bs4 import BeautifulSoup as bs
import yfinance as yf
from producersetup import p, get, yfinance_symbols_dax_companies, delivery_report, all_companies

def get_holder(companies): #benötigt andere Yahoo liste
    for company in companies:
        holders = dict()
        try:
            base_url = f"https://de.finance.yahoo.com/quote/{company}/holders?p={company}"
            soup = bs(get(base_url, True), 'html.parser')

            found_holder = soup.find("div", {"class": "W(100%) Mb(20px)"})

            for row in found_holder.findAll('tr'):
                aux = row.findAll('td')
                holders[aux[1].string] = aux[0].string
        except Exception as e:
            holders = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")
        # Store company as key and WKN/ISIN as value in a dict and transform it into JSON
        # print({company: identification_number})
        p.produce('holder', json.dumps({str(company): holders}), callback=delivery_report)
        p.flush()
    return "Done. Produced all Holder to Kafka."


def get_WKN_and_ISIN(companies: list = all_companies):
    # Scrape finanzen.net for each company for WKN/ ISN
    for company in companies:
        try:
            base_url = f'https://www.finanzen.net/aktien/{company}-aktie'
            soup = bs(get(base_url), 'html.parser')
            identification_numbers = soup.find('span', attrs={'class': 'instrument-id'}).text

        except Exception as e:
            identification_numbers = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and WKN/ISIN as value in a dict and transform it into JSON
        # print({company: identification_number})
        p.produce('wkns_and_isins', json.dumps({str(company): identification_numbers}), callback=delivery_report)
        p.flush()
    return "Done. Produced all WKNs and ISINs to Kafka."

#funktioniert noch nicht ganz
def get_history_stock_price(companies: list = yfinance_symbols_dax_companies):
    # Get ticker for multiple companies
    ticker = initialize_yf_tickers(companies)

    # Iterate over every company and extract Total Sustainability Score
    history_stock_price = dict()

    for company in companies:
        try:
            history_stock_price[f'{company}'] = ticker.history(period='max')
            print("Producing record: {}\t{}".format(company, history_stock_price[f'{company}']))
        except Exception as e:
            record_value = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return history_stock_price

def get_ESG_score(companies: list = yfinance_symbols_dax_companies):
    # Iterate over every company and extract ESG Score
    for company in companies:
        try:
            suffix = '.DE'
            company_ticker = yf.Ticker(f'{company.upper()+suffix}')
            # To create the value in a suitable way, we have to transpose the sustainability data frame
            # in order to extract the Total ESG Score.
            record_value = company_ticker.sustainability.T['totalEsg']['Value']

        except Exception as e:
            record_value = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        p.produce('esg', json.dumps({str(company): record_value}), callback=delivery_report)
        p.flush()
        time.sleep(5)

    return "Done. Produced all ESGs to Kafka."

# We can extract every KPI for each DAX40 company by changing the argument of the get_financial_KPI function.
# Instead of implementing five individual functions with the same structure, we only pass the KPI as an argument.
financial_KPIs = ['Gross Profit', 'Ebit', 'Total Revenue', 'Net Income', 'Total Operating Expenses']

# Convert dictionary keys from given data type to string
def convert_timestamps_keys_to_str(d: dict):
    return {str(k): v for k, v in d.items()}


def get_kpi_topic(kpi: str):
    # Because Confluent Kafka doesn't allow blank spaces within a topic name,
    # we replace the blank space in the kpi's name with an underscore.
    return kpi.replace(" ", "_")


def get_financial_KPI(kpi: str, companies: list = yfinance_symbols_dax_companies, yearly_basis=True):
    # Iterate over every company and extract gross profit development
    for company in companies:
        # Due to some performance issues
        time.sleep(15)
        try:
            # The Suffix is required for finance.yahoo.com, otherwise it won't recognize the symbol
            suffix = '.DE'
            company_ticker = yf.Ticker(f'{company.upper()+suffix}')
            # To create the value in a suitable way, we have to transpose the kpi data frame
            # in order to extract the kpi and its value over the years (since 2019).
            if yearly_basis:
                record_value = company_ticker.financials.T[kpi].to_dict()
            else:
                record_value = company_ticker.quarterly_financials.T[kpi].to_dict()

        except Exception as e:
            record_value = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Because yfinance returns a DataFrame with timestamps as keys, we have to convert them into a string
        # since Timestamps won't work as json key
        record_value = convert_timestamps_keys_to_str(record_value)

        p.produce(get_kpi_topic(kpi), json.dumps({str(company): record_value}), callback=delivery_report)
        p.flush()

    return f"Done. Produced {financial_KPIs} for all DAX40 companies to Kafka."


if __name__ == '__main__':
    # Test if all KPIs are extractable
    print("Now: WKNs and ISINs for all DAX Companies ...")
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
