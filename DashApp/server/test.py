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
db_dax_news = client["Company-Environment"]["dax_news"]


"""def to_df(symbol):
    for item in mongodb.find(
        {"time": {"$gt": f"2022-06-15 15:59:30"}, "company": symbol}
    ):
        if item["stock_price_onehour"] != "NaN":
            data = literal_eval(item["stock_price_onehour"])
            df = pd.DataFrame.from_dict(data)
            # Have to add 2 hours in order to get CEST time right
            df.index = pd.to_datetime(df.index, unit="ms") + timedelta(hours=2)
            print(f"Now company: {item['company']}\n{item['time']}")
            print(df)"""


def concat_dfs(symbol, given_date, given_time):
    result_df = pd.DataFrame()

    # Get History Stock Priceay
    request_history_price = requests.get(
        f"https://bdma-352709.ey.r.appspot.com/stock_price_history/{symbol}"
    ).json()
    history_df = pd.DataFrame.from_dict(literal_eval(request_history_price))
    history_df.index = pd.to_datetime(history_df.index, unit="ms") + timedelta(hours=2)

    request = requests.get(
        f"https://bdma-352709.ey.r.appspot.com/stock_price/{symbol}/{given_date}/{given_time}"
    )
    result_api_call = request.json()

    for package in range(len(result_api_call)):
        data_as_df = pd.DataFrame.from_dict(
            literal_eval(result_api_call[package]["stock_price_onehour"])
        )
        result_df = pd.concat([result_df, data_as_df], axis=0)
    result_df.index = pd.to_datetime(result_df.index, unit="ms") + timedelta(hours=2)
    # print(result_df)
    return pd.concat([history_df, result_df], axis=0)


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

    candlestick_chart.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=4, label="4h", step="hour", stepmode="backward"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    return candlestick_chart.show()


if __name__ == "__main__":
    # print([obj for obj in db_dax_news.find()])
    give_candlestick_chart(concat_dfs("ads", "2022-06-21", "12:00"))
    give_candlestick_chart(concat_dfs("^GDAXI", "2022-06-21", "12:00"))
    # concat_dfs("ads", "2022-06-16")
