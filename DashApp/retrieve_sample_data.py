import pymongo
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

databases = ['kpis', 'news', 'stocks']

# Set up
db_kpi = client['kpis']
db_news = client['news']
db_stocks = client['stocks']

# Set up collections
kpis_collections = ['controversy_level', 'ebitda', 'esg', 'free_cashflow', 'gross_profit', 'revenue']
# kpis_controversy_level = db_kpi['controversy_level']
# kpis_ebitda = db_kpi['ebitda']
# kpis_esg = db_kpi['esg']
# kpis_free_cashflow = db_kpi['free_cashflow']
# kpis_gross_profit = db_kpi['gross_profit']
# kpis_revenue = db_kpi['revenue']

news_collections = ['corporate_news']
# news_corporate_news = db_news['corporate_news']

stocks_collections = ['chart', 'holders', 'marketcap']
# stocks_chart = db_stocks['chart']
# stocks_holders = db_stocks['holders']
# stocks_marketcap = db_stocks['marketcap']

def get_kpi_data():
    all_json = list()
    for collectype in kpis_collections:
        for data in db_kpi[f'{collectype}'].find():
            all_json.append(data)
    return all_json

def get_news_data():
    all_json = list()
    for collectype in news_collections:
        for data in db_news[f'{collectype}'].find():
            all_json.append(data)
    return all_json

def get_stocks_data():
    all_json = list()
    for collectype in stocks_collections:
        for data in db_stocks[f'{collectype}'].find():
            all_json.append(data)
    return all_json


if __name__ == '__main__':
    # test if you get the data
    print(get_kpi_data())
    print(get_news_data())
    print(get_stocks_data())