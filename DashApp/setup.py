import requests


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    return "DONE."


all_companies = [
    "adidas",
    "airbus",
    "allianz",
    "basf",
    "bayer",
    "bmw",
    "brenntag",
    "continental",
    "covestro",
    "daimler_truck",
    "delivery_hero",
    "deutsche_bank",
    "deutsche_boerse",
    "deutsche_post",
    "deutsche_telekom",
    "eon",
    "fresenius",
    "fresenius_medical_care",
    "hannover_rueck",
    "heidelbergcement",
    "hellofresh",
    "henkel_vz",
    "infineon",
    "linde",
    "mercedes-benz",
    "merck",
    "mtu",
    "munich_re",
    "porsche",
    "puma",
    "qiagen",
    "rwe",
    "sap",
    "sartorius_vz",
    "siemens",
    "siemens_healthineers",
    "symrise",
    "volkswagen",
    "vonovia",
    "zalando",
]

companies_url = [
    "adidas",
    "airbus",
    "allianz",
    "basf",
    "bayer",
    "bmw",
    "brenntag",
    "continental",
    "covestro",
    "daimler-truck",
    "deliveryhero",
    "deutsche-bank",
    "deutsche-boerse",
    "deutschepost",
    "telekom",
    "eon",
    "fresenius",
    "freseniusmedicalcare",
    "hannover-rueck",
    "heidelbergcement",
    "hellofresh",
    "henkel",
    "infineon",
    "linde-gas",
    "mercedes-benz",
    "merckgroup",
    "mtu",
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
    "volkswagen",
    "vonovia",
    "zalando",
]


# Source for DAX Symbols: https://de.wikipedia.org/wiki/DAX#Zusammensetzung
yfinance_symbols_dax_companies = [
    "ads",
    "air",
    "alv",
    "bas",
    "bayn",
    "bmw",
    "bnr",
    "con",
    "1cov",
    "dtg",
    "dher",
    "dbk",
    "db1",
    "dpw",
    "dte",
    "eoan",
    "fre",
    "fme",
    "hnr1",
    "hei",
    "hfg",
    "hen3",
    "ifx",
    "lin",
    "mbg",
    "mrk",
    "mtx",
    "muv2",
    "pah3",
    "pum",
    "qia",
    "rwe",
    "sap",
    "srt3",
    "sie",
    "shl",
    "sy1",
    "vow3",
    "vna",
    "zal",
]

kununu_companies = [
    "adidas",
    "airbus",
    "allianzdeutschland",
    "basf-se",
    "bayer",
    "bmwgroup",
    "brenntag",
    "continental-gruppe",
    "covestro-deutschland3",
    "daimler-truck3",
    "delivery-hero",
    "deutsche-bank",
    "deutsche-boerse",
    "deutsche-post",
    "deutsche-telekom",
    "eon",
    "fresenius-se",
    "fresenius-medical-care",
    "hannover-rueckversicherung",
    "heidelberg-zement",
    "hellofresh",
    "henkel-aa",
    "infineon-technologies",
    "linde",
    "mercedes-benz-group",
    "merckaa",
    "mtuaeroengines",
    "muenchener-rueckversicherung",
    "porsche-gruppe",
    "pumagroup",
    "qiagen",
    "rwe",
    "sap",
    "sartorius",
    "siemens",
    "siemens-healthineers-austria",
    "symrise",
    "volkswagen",
    "vonovia-se",
    "zalando",
]

community_company = [
    "adidas",
    "airbus",
    "allianz",
    "basf",
    "bayer",
    "bmw",
    "brenntag",
    "continental",
    "covestro",
    "daimler-truck-holding",
    "delivery-hero",
    "deutsche-bank",
    "deutsche-boerse",
    "deutsche-post",
    "deutsche-telekom",
    "e-on",
    "fresenius",
    "fresenius-medical-care",
    "hannover-rueck",
    "heidelbergcement",
    "hellofresh",
    "henkel-vz",
    "infineon-technologies",
    "linde",
    "mercedes-benz-group",
    "merck",
    "mtu-aero-engines",
    "m-nchener-r-ck",
    "porsche",
    "puma",
    "qiagen",
    "rwe",
    "sap",
    "sartorius",
    "siemens",
    "siemens-healthineers",
    "symrise",
    "volkswagen-vw-vz",
    "vonovia",
    "zalando",
]

community_number = [
    "109",
    "40",
    "715",
    "364",
    "1084",
    "394",
    "6442",
    "130",
    "6289",
    "74246",
    "15223",
    "4",
    "2263",
    "7",
    "148",
    "310",
    "1654",
    "1489",
    "3313",
    "226",
    "17599",
    "367",
    "211",
    "22663",
    "91",
    "2635",
    "5578",
    "634",
    "277",
    "2749",
    "1726",
    "505",
    "118",
    "1072",
    "256",
    "19858",
    "1006",
    "385",
    "2413",
    "2692",
]

test_symbols = ["ads", "air", "alv"]


timezone= ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00',
             '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']


# Crawling web page with given URL
# param :yahoo_finance: To crawl data from yahooFinance, we have to send a User-Agent Header, otherwise YF will block the request
def get(url, yahoo_finance=False):
    yahoo_finance_header = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    if yahoo_finance:
        res = requests.get(url, headers=yahoo_finance_header)
    else:
        res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        raise BaseException


def create_company_dict(
    company_names: list = all_companies, symbols: list = yfinance_symbols_dax_companies
):
    company_dict = {}
    for index in range(len(company_names)):
        company_dict[company_names[index]] = symbols[index]
    return company_dict

def create_company_dict_kununu(
    company_names: list = all_companies, symbols: list = kununu_companies
):
    company_dict = {}
    for index in range(len(company_names)):
        company_dict[company_names[index]] = symbols[index]
    return company_dict

def create_company_dict_community(
    company_names: list = all_companies, symbols: list = community_company
):
    company_dict = {}
    for index in range(len(company_names)):
        company_dict[company_names[index]] = symbols[index]
    return company_dict

if __name__ == "__main__":
    print(len(yfinance_symbols_dax_companies))
    print(len(all_companies))
    print(len(companies_url))
    print(len(community_number))
    print(len(community_company))
    print(len(community_company) == len(community_number))
