"""
Here we will extract data from the internet which won't change in June 2022
"""


from bs4 import BeautifulSoup as bs
# from producer import initialize_yf_tickers, get
import yfinance
import requests
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

yfinance_symbols_dax_companies = [
     'ads', 'air', 'alv', 'bas', 'bayn', 'bmw', 'bnr',
     'con', '1cov', 'dtg', 'dher', 'dbk', 'db1', 'dpw',
     'dte', 'eoan', 'fre', 'fme', 'hnr1', 'hei', 'hfg',
     'hen3', 'ifx', 'lin', 'mbg', 'mrk', 'mtx', 'muv2',
     'pah3', 'pum', 'qia', 'rwe', 'sap', 'srt3', 'sie',
     'shl', 'sy1', 'vow3', 'vna', 'zal'
]

yahoo_finance_header = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

# Crawling web page with given URL
def get(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        return f'Error in URL Status Code: ERROR {res.status_code}'


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

    return all_wkns_and_isins

def get_EBITDA(companies: list = yfinance_symbols_dax_companies):
    for company in companies:
        print(f"{company.upper() + '.DE'}: 1")
        url = f"https://de.finance.yahoo.com/quote/{company.upper()+'.DE'}/key-statistics?p={company.upper()+'.DE'}"
        soup = bs(get(url), header=yahoo_finance_header, parser='html.parser')
        ebitda = soup.find("td", attrs={'class':'Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px)'})
        # p.send(topic, key=f"{company}", value=ebitda.findChild('span').text)
        print(f"{company.upper()+'.DE'}: 1")

if __name__ == '__main__':
    #print(get_WKN_and_ISIN(all_companies))
    get_EBITDA()
