import pandas as pd
import pymongo
import certifi
from flask import Flask
from flask_restx import Resource, Api
from datetime import datetime, timedelta, date
import re
import json
from io import StringIO
from ast import literal_eval
import requests
from pyrsistent import v
import plotly as plt
import plotly.graph_objects as go


client = pymongo.MongoClient(
    "mongodb+srv://allguys:M2Ju99giul6Hwlg2@bdma.rvryhyj.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

mongodb = client["Investor-Relations"]["stock_price_lasthour"]


def to_df(symbol):
    for item in mongodb.find(
        {"time": {"$gt": "2022-06-15 15:59:30"}, "company": symbol}
    ):
        if item["stock_price_onehour"] != "NaN":
            data = literal_eval(item["stock_price_onehour"])
            df = pd.DataFrame.from_dict(data)
            # Have to add 2 hours in order to get CEST time right
            df.index = pd.to_datetime(df.index, unit="ms") + timedelta(hours=2)
            print(f"Now company: {item['company']}\n{item['time']}")
            print(df)


def concat_dfs(symbol, given_date):
    request = requests.get(
        f"http://127.0.0.1:5000/stock_price_over_period/{symbol}/{given_date}"
    )
    result_api_call = request.json()
    result_df = pd.DataFrame()
    for package in range(len(result_api_call)):
        data_as_df = pd.DataFrame.from_dict(
            literal_eval(result_api_call[package]["stock_price_onehour"])
        )
        result_df = pd.concat([result_df, data_as_df], axis=0)
    result_df.index = pd.to_datetime(result_df.index, unit="ms") + timedelta(hours=2)
    # print(result_df)
    return result_df


def give_candlestick_chart(df: pd.DataFrame):
    candlestick_chart = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )
    return candlestick_chart.show()


if __name__ == "__main__":
    give_candlestick_chart(concat_dfs("ads", "2022-06-16"))
    give_candlestick_chart(concat_dfs("^GDAXI", "2022-06-16"))
