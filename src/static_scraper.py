"""
Here we will extract data from the internet which won't change in June 2022
"""
import time
from bs4 import BeautifulSoup as bs
import yfinance as yf
from producersetup import get, yfinance_symbols_dax_companies, topic, delivery_report, all_companies


def get_WKN_and_ISIN(companies: list = all_companies):
    all_wkns_and_isins = dict()
    # Scrape finanzen.net for each company for WKN/ ISN
    for company in companies:
        try:
            base_url = f'https://www.finanzen.net/aktien/{company}-aktie'
            soup = bs(get(base_url), 'html.parser')
            # Siehe https://www.finanzen.net/aktien/{company}-aktie
            identification_number = soup.find('span', attrs={'class': 'instrument-id'})
            #Store company as key and WKN/ISIN as value
            all_wkns_and_isins[f'{company}'] = identification_number.text
            #p.produce(topic, json.dumps(dict({company: all_wkns_and_isins[f'{company}']})), callback=delivery_report)
            #p.flush()
        except Exception as e:
            all_wkns_and_isins[f'{company}'] = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

    return all_wkns_and_isins


def get_ESG_score(companies: list = yfinance_symbols_dax_companies):
    # Iterate over every company and extract ESG Score
    for company in companies:
        try:
            suffix = '.DE'
            company_ticker = yf.Ticker(f'{company.upper()+suffix}')
            # To create the value in a suitable way, we have to transpose the sustainability data frame
            # in order to extract the Total ESG Score.
            record_value = company_ticker.sustainability.T['totalEsg'].to_dict()
            post = {f'{company}': record_value}
            print(post)
        except Exception as e:
            record_value = 'NaN'
            post = {f'{company}': record_value}
            print(f"FAILED. For {company} the following error occured: {type(e)}")
            print(post)
            continue
    return "Done. Produced all ESGs to Kafka."

# We can extract every KPI for each DAX40 company by changing the argument of the get_financial_KPI function.
# Instead of implementing five individual functions with the same structure, we only pass the KPI as an argument.
financial_KPIs = ['Gross Profit', 'Ebit', 'Total Revenue', 'Net Income', 'Total Operating Expenses']

def get_financial_KPI(kpi: str, companies: list = yfinance_symbols_dax_companies):
    # Iterate over every company and extract gross profit development
    for company in companies:
        time.sleep(12)
        try:
            # The Suffix is required for finance.yahoo.com, otherwise it won't recognize the symbol
            suffix = '.DE'
            company_ticker = yf.Ticker(f'{company.upper()+suffix}')
            # To create the value in a suitable way, we have to transpose the kpi data frame
            # in order to extract the kpi and its value over the years (since 2019).
            record_value = company_ticker.financials.T[kpi].to_dict()
            post = {f'{company}': record_value}
            print(post)
        except Exception as e:
            record_value = 'NaN'
            post = {f'{company}': record_value}
            print(f"FAILED. For {company} the following error occured: {type(e)}")
            print(post)
            continue
    return f"Done. Produced {kpi.upper()} for all DAX40 companies to Kafka."


if __name__ == '__main__':
    # Test if all KPIs are extractable
    # print(get_WKN_and_ISIN())
    # get_ESG_score()
    for kpi in financial_KPIs:
        print(f"Now extracting {kpi}. Wait ...")
        time.sleep(30)
        print(f"Listing now all DAX40 companies with all {kpi.upper()} values.\n")
        get_financial_KPI(kpi)
