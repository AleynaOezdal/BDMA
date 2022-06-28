import pandas as pd
import pymongo
import os

from dotenv import load_dotenv  # Not neccessary for GCP AE
import certifi
import pprint as pp
from flask import Flask
from flask_restx import Resource, Api
import json
from datetime import datetime, timedelta
from ast import literal_eval
import re


# Building a restful API with flask-restx
app = Flask(__name__)
api = Api(app)


load_dotenv()  # Not neccessary for GCP AE

client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv("MONGODB.USERNAME")}:{os.getenv("MONGODB.PASSWORD")}@{os.getenv("MONGODB.URI")}/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

# Databases and Collection Setup
db_wkns_and_isins = client["KPIs"]["wkns_and_isins"]
db_esg = client["KPIs"]["esg"]
db_total_revenue = client["KPIs"]["total_revenue"]
db_total_operating_expenses = client["KPIs"]["total_operating_expenses"]
db_net_income = client["KPIs"]["net_income"]
db_gross_profit = client["KPIs"]["gross_profit"]
db_ebit = client["KPIs"]["ebit"]
db_description = client["KPIs"]["company_description"]
db_distribution = client["KPIs"]["industry_with_competitors"]

db_major_holders = client["Investor-Relations"]["major_holders"]
db_dividends = client["KPIs"]["dividends"]
db_history_stock_price = client["Investor-Relations"]["history_stock_price"]
db_key_characteristics = client["Investor-Relations"]["key_characteristics"]
db_stock_price_lasthour = client["Investor-Relations"]["stock_price_lasthour"]
# db_key_characteristics tbd
# db_company_stock_data tbd
# db_dax_stock_data tbd
# + API

db_world_news = client["Company-Environment"]["world_news"]
db_company_news = client["Company-Environment"]["company_news_gcp"]
db_worker_reviews = client["Company-Environment"]["worker_reviews"]
db_customer_experience = client["Company-Environment"]["customer_exp_gcp"]
db_community_news = client["Company-Environment"]["community_news_gcp"]
db_weather = client["Company-Environment"]["weather"]
db_international_dax_news = client["Company-Environment"]["international_dax_news"]
db_dax_news = client["Company-Environment"]["dax_news"]

# Get WKN and ISIN for a company
class WKN(Resource):
    def get(self, company):
        return db_wkns_and_isins.find_one({"company": company})["wkns_and_isins"]


# Get ESG Score for a company
class ESG(Resource):
    def get(self, symbol):
        return db_esg.find_one({"company": symbol})["esg_score"]


# Get Total Revenue for a company
class TotalRevenue(Resource):
    def get(self, symbol):
        result = db_total_revenue.find_one({"company": symbol})["Total Revenue"]
        # return pd.DataFrame(result, index=["Total Revenue"]).T
        return result


# Get Total Operating Expenses for a company
class TotalOperatingExpenses(Resource):
    def get(self, symbol):
        result = db_total_operating_expenses.find_one({"company": symbol})[
            "Total Operating Expenses"
        ]
        # return pd.DataFrame(result, index=["Total Operating Expenses"]).T
        return result


# Get Net Income for a company
class NetIncome(Resource):
    def get(self, symbol):
        result = db_net_income.find_one({"company": symbol})["Net Income"]
        return result


# Get Gross Profit for a company
class GrossProfit(Resource):
    def get(self, symbol):
        result = db_gross_profit.find_one({"company": symbol})["Gross Profit"]
        return result


# Get EBIT for a company
class EBIT(Resource):
    def get(self, symbol):
        result = db_ebit.find_one({"company": symbol})["Ebit"]
        return result


# Get Description for a company
class Description(Resource):
    def get(self, company):
        return db_description.find_one({"company": company})["company_description"]


# Get Industry in which a company is active
class IndustryDistribution(Resource):
    def get(self, company):
        return db_distribution.find_one({"corporates_in_industry": company})["industry"]


# Get Main Competitors of a company
class MainCompetitors(Resource):
    def get(self, company):
        return db_distribution.find_one({"corporates_in_industry": company})[
            "corporates_in_industry"
        ]


class MajorHolders(Resource):
    def get(self, symbol):
        return db_major_holders.find_one({"company": symbol})["holders"]


class Dividends(Resource):
    def get(self, symbol):
        return db_dividends.find_one({"company": symbol})["dividends"]


class KeyCharacteristics(Resource):
    def get(self, company, date, time):
        cursor = (
            db_key_characteristics.find(
                {
                    "company": company,
                    "time": {"$lte": date + " " + time + ":59"},
                }
            )
            .limit(1)
            .sort([("$natural", -1)])
        )
        for item in cursor:
            return item["key_characteristics"][f"{company}"]


class HistoryStockPrice(Resource):
    def get(self, symbol):
        return db_history_stock_price.find_one({"company": symbol})[
            "history_stock_price"
        ]


class StockPriceOverPeriod(Resource):
    def get(self, symbol, date, time):
        result = list()
        time_string = date + " " + time
        query = db_stock_price_lasthour.find(
            {"time": {"$lt": time_string}, "company": symbol}
        )
        for data in query:
            del data["_id"]
            result.append(data)
        return result


class AllWorldNewsByDate(Resource):
    def get(self, date, time):
        cursor = (
            db_world_news.find({"time": {"$lte": date + " " + time + ":59"}})
            .limit(25)
            .sort([("$natural", -1)])
        )
        result = list()
        for item in cursor:
            del item["_id"]
            result.append(item)
        return result


class CompanyNews(Resource):
    def get(self, company, date, time):
        cursor = (
            db_company_news.find(
                {"company": company, "timestamp": {"$lte": date + " " + time + ":59"}}
            )
            .limit(25)
            .sort([("$natural", -1)])
        )
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class CompanyNews24h(Resource):
    def get(self, company, date, time):
        today_strtime = date + " " + time + ":59"
        today_date = datetime.strptime(today_strtime, "%Y-%m-%d %H:%M:%S")
        yesterday_date = today_date - timedelta(days=1.0, minutes=1.0)
        yesterday_strtime = datetime.strftime(yesterday_date, "%Y-%m-%d %H:%M:%S")
        cursor = db_company_news.find(
            {
                "company": company,
                "$and": [
                    {"timestamp": {"$lte": today_strtime}},
                    {"timestamp": {"$gte": yesterday_strtime}},
                ],
            }
        ).sort([("$natural", -1)])
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class Reviews(Resource):
    def get(self, company, date, time):
        cursor = (
            db_worker_reviews.find(
                {"company": company, "time": {"$lte": date + " " + time + ":59"}}
            )
            .limit(25)
            .sort([("$natural", -1)])
        )
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class CustomerExperience(Resource):
    def get(self, company, date, time):
        cursor = (
            db_customer_experience.find(
                {"company": company, "timestamp": {"$lte": date + " " + time + ":59"}}
            )
            .limit(25)
            .sort([("$natural", -1)])
        )
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class CustomerExperience24h(Resource):
    def get(self, company, date, time):
        today_strtime = date + " " + time + ":59"
        today_date = datetime.strptime(today_strtime, "%Y-%m-%d %H:%M:%S")
        yesterday_date = today_date - timedelta(days=1.0, minutes=1.0)
        yesterday_strtime = datetime.strftime(yesterday_date, "%Y-%m-%d %H:%M:%S")
        cursor = db_customer_experience.find(
            {
                "company": company,
                "$and": [
                    {"timestamp": {"$lte": today_strtime}},
                    {"timestamp": {"$gte": yesterday_strtime}},
                ],
            }
        ).sort([("$natural", -1)])
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class CommunityNewsForCompany(Resource):
    def get(self, company, date, time):
        cursor = (
            db_community_news.find(
                {"company": company, "timestamp": {"$lte": date + " " + time + ":59"}}
            )
            .limit(25)
            .sort([("$natural", -1)])
        )
        community_posts = []
        for obj in cursor:
            del obj["_id"]
            community_posts.append(obj)
        return community_posts


class CommunityNewsForCompany24h(Resource):
    def get(self, company, date, time):
        today_strtime = date + " " + time + ":59"
        today_date = datetime.strptime(today_strtime, "%Y-%m-%d %H:%M:%S")
        yesterday_date = today_date - timedelta(days=1.0, minutes=1.0)
        yesterday_strtime = datetime.strftime(yesterday_date, "%Y-%m-%d %H:%M:%S")
        cursor = db_community_news.find(
            {
                "company": company,
                "$and": [
                    {"timestamp": {"$lte": today_strtime}},
                    {"timestamp": {"$gte": yesterday_strtime}},
                ],
            }
        ).sort([("$natural", -1)])
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class Weather(Resource):
    def get(self, city, date, time):
        cursor = (
            db_weather.find({"city": city, "time": {"$lte": date + " " + time + ":59"}})
            .limit(1)
            .sort([("$natural", -1)])
        )
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class InternationalDaxNews(Resource):
    def get(self, date, time):
        cursor = (
            db_international_dax_news.find(
                {"time": {"$lte": date + " " + time + ":59"}}
            )
            .limit(25)
            .sort([("$natural", -1)])
        )
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


class DAXNews(Resource):
    def get(self, date, time):
        cursor = (
            db_dax_news.find({"time": {"$lte": date + " " + time + ":59"}})
            .limit(25)
            .sort([("$natural", -1)])
        )
        result = []
        for obj in cursor:
            del obj["_id"]
            result.append(obj)
        return result


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
# Status: No problems, all working
api.add_resource(MajorHolders, "/major_holders/<symbol>")
api.add_resource(Dividends, "/dividends/<symbol>")
api.add_resource(KeyCharacteristics, "/key_characteristics/<company>/<date>/<time>")
api.add_resource(HistoryStockPrice, "/stock_price_history/<symbol>")
api.add_resource(StockPriceOverPeriod, "/stock_price/<symbol>/<date>/<time>")


# Dashboard: Company Environment
# Status: No problems, all working
api.add_resource(AllWorldNewsByDate, "/world_news_by_date/<date>/<time>")
api.add_resource(CompanyNews, "/company_news_classified/<company>/<date>/<time>")
api.add_resource(CompanyNews24h, "/company_news_classified_24h/<company>/<date>/<time>")
api.add_resource(Reviews, "/worker_reviews/<company>/<date>/<time>")
api.add_resource(CustomerExperience, "/customer_experience/<company>/<date>/<time>")
api.add_resource(
    CustomerExperience24h, "/customer_experience_24h/<company>/<date>/<time>"
)
api.add_resource(CommunityNewsForCompany, "/community_news/<company>/<date>/<time>")
api.add_resource(
    CommunityNewsForCompany24h, "/community_news_24h/<company>/<date>/<time>"
)
api.add_resource(Weather, "/weather/<city>/<date>/<time>")
api.add_resource(InternationalDaxNews, "/international_dax_news/<date>/<time>")
api.add_resource(DAXNews, "/dax_news/<date>/<time>")


if __name__ == "__main__":
    # test if you get the data
    app.run(debug=False)
