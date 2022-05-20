"""
Here we will extract data from the internet which won't change in June 2022
"""


from bs4 import BeautifulSoup as bs
from scraper import yfinance_symbols_dax_companies, initialize_yf_tickers, get
# from producersetup import p, topic, delivery_report
# import json


all_companies = [
    'adidas', 'airbus', 'allianz', 'basf', 'bayer', 'bmw', 'brenntag',
    'continental', 'covestro', 'daimler_truck', 'delivery_hero', 'deutsche_bank',
    'deutsche_boerse', 'deutsche_post', 'deutsche_telekom', 'eon', 'fresenius',
    'fresenius_medical_care', 'hannover_rueck', 'heidelbergcement', 'hellofresh',
    'henkel_vz', 'infineon', 'linde', 'mercedes-benz', 'porsche', 'puma', 'qiagen',
    'rwe', 'sap', 'sartorius_vz', 'siemens', 'siemens_healthineers', 'symrise',
    'volkswagen', 'vonovia', 'zalando'
]


def get_WKN_and_ISIN(companies: list = ['adidas', 'volkswagen']):
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

    return True

if __name__ == '__main__':
    print(get_WKN_and_ISIN(all_companies))