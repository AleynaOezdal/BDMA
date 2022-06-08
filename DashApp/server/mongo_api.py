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
import re

from requests import head

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
# db_key_characteristics tbd
# db_company_stock_data tbd
# db_dax_stock_data tbd
# + API

db_world_news = client["Company-Experience"]["world_news"]
db_company_news = client["Company-Experience"]["company_news_sentiment"]
db_reviews = client["Company-Experience"]["Reviews"]
db_customer_experience = client["Company-Experience"]["Customer_experience_sentiment"]
db_community_news = client["Company-Experience"]["Community_news_sentiment"]
# db_dax_news


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


class DAXStockDataLowerBorder(Resource):
    def get(self, YYYY_MM_DD: str):
        courses = db_dax_history_stock_data.find({"stock_date": {"$gt": YYYY_MM_DD}})
        return [stock_day for stock_day in courses]


class AllWorldNewsByDate(Resource):
    def get(self):
        cursor = db_world_news.find({"time": {"$gt": datetime.today() - timedelta(30)}})
        queries = [object for object in cursor]
        return queries


class CompanyNews(Resource):
    def get(self, company):
        cursor = db_company_news.find(
            {"id": {"$regex": re.escape(company) + r"_[0-9]*"}}
        )
        headlines_for_company = []
        for obj in cursor:
            del obj["_id"]
            headlines_for_company.append(obj)
        return headlines_for_company


class Reviews(Resource):
    def get(self, company):
        cursor = db_reviews.find({"_id": {"$regex": re.escape(company) + r"_[0-9]*"}})
        return [obj for obj in cursor]


class CustomerExperience(Resource):
    def get(self, company):
        cursor = db_customer_experience.find(
            {"id": {"$regex": re.escape(company) + r"_[0-9]*"}}
        )
        customer_experience = []
        for obj in cursor:
            del obj["_id"]
            customer_experience.append(obj)
        return customer_experience


class CommunityNewsForCompany(Resource):
    def get(self, company):
        cursor = db_community_news.find(
            {"id": {"$regex": re.escape(company) + r"_[0-9]*"}}
        )
        community_posts = []
        for obj in cursor:
            del obj["_id"]
            community_posts.append(obj)
        return community_posts


# Add our API Endpoints
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
api.add_resource(DAXStockDataLowerBorder, "/dax_data_per_day/<YYYY_MM_DD>")

# Dashboard: Company Environment
# Status: to be tested
api.add_resource(AllWorldNewsByDate, "/world_news_by_date")
api.add_resource(CompanyNews, "/company_news_classified/<company>")
api.add_resource(Reviews, "/reviews/<company>")
api.add_resource(CustomerExperience, "/customer_experience/<company>")
api.add_resource(CommunityNewsForCompany, "/community_news/<company>")


if __name__ == "__main__":
    # test if you get the data
    app.run(debug=True)
