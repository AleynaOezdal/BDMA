import pandas as pd
import pymongo
import os
from dotenv import load_dotenv
import certifi
import pprint as pp
from flask import Flask
from flask_restx import Resource, Api
import json
from datetime import datetime, timedelta

# Building a restful API with flask-restx
app = Flask(__name__)
api = Api(app)


load_dotenv()

client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

# Databases and Collection Setup
db_wkns_and_isins = client["KPIs"]["wkns_and_isins"]
db_esg = client["KPIs"]["esg"]
db_total_revenue = client["KPIs"]["Total_Revenue"]
db_total_operating_expenses = client["KPIs"]["Total_Operating_Expenses"]
db_net_income = client["KPIs"]["Net_Income"]
db_gross_profit = client["KPIs"]["Gross_Profit"]
db_ebit = client["KPIs"]["Ebit"]
db_description = client["KPIs"]["company_description"]
db_distribution = client["KPIs"]["dax40_distribution"]

db_holders = client["Investor-Relations"]["holders"]
db_dividends = client["Investor-Relations"]["dividends"]
db_dax_history_stock_data = client["Investor-Relations"]["dax_history_stock_data"]

db_world_news = client["Company-Experience"]["world_news"]
db_company_news = client["Company-Experience"]["company_news"]
db_reviews = client["Company-Experience"]["reviews"]
db_customer_experience = client["Company-Experience"]["customer_experience"]
db_community_news = client["Company-Experience"]["community_news"]


# Get WKN and ISIN for a company
class WKN(Resource):
    def get(self, company):
        return db_wkns_and_isins.find_one({"_id": company})["wkns_and_isins"]


# Get ESG Score for a company
class ESG(Resource):
    def get(self, symbol):
        return db_esg.find_one({"_id": symbol})["esg_score"]


# Get Total Revenue for a company
class TotalRevenue(Resource):
    def get(self, symbol):
        result = db_total_revenue.find_one({"_id": symbol})["Total Revenue"]
        # return pd.DataFrame(result, index=["Total Revenue"]).T
        return result


# Get Total Operating Expenses for a company
class TotalOperatingExpenses(Resource):
    def get(self, symbol):
        result = db_total_operating_expenses.find_one({"_id": symbol})[
            "Total Operating Expenses"
        ]
        # return pd.DataFrame(result, index=["Total Operating Expenses"]).T
        return result


# Get Net Income for a company
class NetIncome(Resource):
    def get(self, symbol):
        result = db_net_income.find_one({"_id": symbol})["Net Income"]
        return result


# Get Gross Profit for a company
class GrossProfit(Resource):
    def get(self, symbol):
        result = db_gross_profit.find_one({"_id": symbol})["Gross Profit"]
        return result


# Get EBIT for a company
class EBIT(Resource):
    def get(self, symbol):
        result = db_ebit.find_one({"_id": symbol})["Ebit"]
        return result


# Get Description for a company
class Description(Resource):
    def get(self, company):
        return db_description.find_one({"_id": company})["company_description"]


# Get Industry in which a company is active
class IndustryDistribution(Resource):
    def get(self, company):
        return db_distribution.find_one({"corporates_in_industry": company})["_id"]


# Get Main Competitors of a company
class MainCompetitors(Resource):
    def get(self, company):
        return db_distribution.find_one({"corporates_in_industry": company})[
            "corporates_in_industry"
        ]


class MajorHolders(Resource):
    def get(self, symbol):
        return db_holders.find_one({"_id": symbol})["holders"]


class Dividends(Resource):
    def get(self, symbol):
        return db_dividends.find_one({"_id": symbol})["dividends"]


class DAXStockDataByDay(Resource):
    def get(self, date):
        return db_dax_history_stock_data.find_one({"stock_date": date})[
            "stock_history_til_date"
        ]


class AllWorldNewsByDate(Resource):
    def get(self):
        cursor = db_world_news.find({"time": {"$gt": datetime.today() - timedelta(30)}})
        queries = [object for object in cursor]
        return queries


# Add our API Endpoints to the FLASK APIs
# Dashboard: Key Performance Indicators
# Status: No problems, all working
api.add_resource(WKN, "/wkns_and_isins/<company>")
api.add_resource(ESG, "/esg_score/<symbol>")
api.add_resource(TotalRevenue, "/total_revenue/<symbol>")
api.add_resource(TotalOperatingExpenses, "/total_operating_expenses/<symbol>")
api.add_resource(NetIncome, "/net_income/<symbol>")
api.add_resource(GrossProfit, "/gross_profit/<symbol>")
api.add_resource(EBIT, "/ebit/<symbol>")
api.add_resource(Description, "/description/<company>")
api.add_resource(IndustryDistribution, "/industry_distribution/<company>")
api.add_resource(MainCompetitors, "/main_competitors/<company>")


# Dashboard: Investor Relations
# Status:  to be tested
api.add_resource(MajorHolders, "/major_holders/<symbol>")
api.add_resource(Dividends, "/dividends/<symbol>")
api.add_resource(DAXStockDataByDay, "/dax_data_per_day/<date>")

# Dashboard: Company Environment
# Status: to be tested
api.add_resource(AllWorldNewsByDate, "/world_news_by_date")


if __name__ == "__main__":
    # test if you get the data
    app.run(debug=True)
