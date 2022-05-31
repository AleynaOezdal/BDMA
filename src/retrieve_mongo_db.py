import pandas as pd
import pymongo
import os
from dotenv import load_dotenv
import certifi
from producersetup import all_companies, get
import pprint as pp

load_dotenv()

client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

# Databses and Collection Setup
db_wkns_and_isins = client["KPIs"]["wkns_and_isins"]
db_esg = client["KPIs"]["esg"]
db_total_revenue = client["KPIs"]["Total_Revenue"]
db_total_operating_expenses = client["KPIs"]["Total_Operating_Expenses"]
db_net_income = client["KPIs"]["Net_Income"]
db_gross_profit = client["KPIs"]["Gross_Profit"]
db_ebit = client["KPIs"]["Ebit"]

db_holders = client["Investor-Relations"]["holders"]
db_dividends = client["Investor-Relations"]["dividends"]
db_dax_history_stock_data = client["Investor-Relations"]["dax_history_stock_data"]

db_world_news = client["Company-Experience"]["world_news"]
db_company_news = client["Company-Experience"]["company_news"]
db_reviews = client["Company-Experience"]["reviews"]
db_customer_experience = client["Company-Experience"]["customer_experience"]
db_community_news = client["Company-Experience"]["community_news"]


def get_wkns_and_isins(company: str):
    return db_wkns_and_isins.find_one({"_id": company})["wkns_and_isins"]


def get_esg_score(symbol: str):
    return db_esg.find_one({"_id": symbol})["esg_score"]


def get_total_revenue(symbol: str) -> pd.DataFrame:
    result = db_total_revenue.find_one({"_id": symbol})["Total Revenue"]
    return pd.DataFrame(result, index=["Total Revenue"]).T


def get_total_operating_expenses(symbol: str) -> pd.DataFrame:
    result = db_total_operating_expenses.find_one({"_id": symbol})[
        "Total Operating Expenses"
    ]
    return pd.DataFrame(result, index=["Total Operating Expenses"]).T


def get_net_income(symbol: str) -> pd.DataFrame:
    result = db_net_income.find_one({"_id": symbol})["Net Income"]
    return pd.DataFrame(result, index=["Net Income"]).T


def get_gross_profit(symbol: str) -> pd.DataFrame:
    result = db_gross_profit.find_one({"_id": symbol})["Gross Profit"]
    return pd.DataFrame(result, index=["Gross Profit"]).T


def get_ebit(symbol: str) -> pd.DataFrame:
    result = db_ebit.find_one({"_id": symbol})["Ebit"]
    return pd.DataFrame(result, index=["Ebit"]).T


if __name__ == "__main__":
    # test if you get the data
    pp.pprint(f"adidas: {get_wkns_and_isins('adidas')}")
    pp.pprint(f"vow3:  {get_esg_score('vow3')}")
    pp.pprint(f"zal: {get_total_revenue('zal')}")
    pp.pprint(f"bmw: {get_total_operating_expenses('bmw')}")
    pp.pprint(f"sap: {get_net_income('sap')}")
    pp.pprint(f"muv2:{get_gross_profit('muv2')}")
    pp.pprint(f"ifx: {get_ebit('ifx')}")
