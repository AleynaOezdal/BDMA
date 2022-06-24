from dash import dcc, html
import plotly.express as px
import pandas as pd
import requests as req
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from setup import create_company_dict
from ast import literal_eval
from datetime import datetime, timedelta, date




company_dict = create_company_dict()


def api_call_date_time(data, date, time):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{date}/{time}"
    result = req.get(url)
    return result.json()

def api_call_value_date_time(data, value, date, time):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{value}/{date}/{time}"
    result = req.get(url)
    return result.json()

def normalize_data(df):
    # df on input should contain only one column with the price data (plus dataframe index)
    min = df.min()
    max = df.max()
    x = df

    # time series normalization part
    # y will be a column in a dataframe
    y = (x - min) / (max - min) * 100

    return y

def get_home_content(value, date, time):
    # value for header
    name = value

    # small letter for dict
    if " " in value:
        value = value.replace(" ", "_")
    if "." in value:
        value = value.replace(".", "")

    value = value.lower()

    content_header_home = html.Div(
        id="content_header_kpi",
        children=[
            html.H3(
                id="content_header_first", children=["Willkommen auf unserem Dashboard"]
            ),
            html.Br(),
            html.P(
                id="content_header_first", children=["Der aktuelle DAX mit den wichtigsten/passenden News:"]
            ),
        ],
    )

    #Dax-Chart
    dax_api_call = api_call_value_date_time("stock_price", "^GDAXI", date, time)
    fig = go.Figure()

    dax_stock = pd.DataFrame()
    for package in range(len(dax_api_call)):
        data_as_df = pd.DataFrame.from_dict(
            literal_eval(dax_api_call[package]["stock_price_onehour"])
        )
        dax_stock = pd.concat([dax_stock, data_as_df], axis=0)
    dax_stock.index = pd.to_datetime(dax_stock.index, unit="ms") + timedelta(hours=2)

    normalized_dax = normalize_data(dax_stock)



    trace2 = go.Scatter(x=normalized_dax.index, y=normalized_dax["High"], opacity=0.7, line=dict(color='blue', width=2),
                        name="DAX")


    fig.add_trace(trace2)

    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            dict(values=["2022-06-19"]),
            dict(bounds=[17.30, 9], pattern="hour"),
        ],
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    #widget Dax-Chart

    widget_dax = html.Div(id='home_widget', children=[
        html.Div(
            id="stocks_widget_text",
            children=[
                html.P(id="stocks_widget_header", children="DAX-Chart")
            ], ),
        html.Div(id='home_graph', children=[
            dcc.Graph(
                figure=fig,
            ),
        ], )

    ], )

    # Dax News
    dax_news_date_time = api_call_date_time('dax_news', date, time)
    dax_news = []

    for entry in dax_news_date_time:
        dax_news.append(entry['news'])

    df_dax_news = pd.DataFrame(dax_news)
    dax_news_dataframe = pd.DataFrame()
    dax_news_dataframe[' '] = df_dax_news['headline']
    dax_news_dataframe['Zeitpunkt'] = df_dax_news['timestamp']

    # widget-four-news
    widget_dax_news = html.Div(
        id="home_widget",
        children=[
            html.Div(
                id="news_widget_content",
                children=[
                    html.H6(id="news_widget_header", children="DAX-News"),
                    html.Div(children=[
                        dbc.Table.from_dataframe(dax_news_dataframe[0:6])
                    ]),
                ]
            )
        ],
    )

    content_home = html.Div(
        id="content_home",
        children=[
            content_header_home,
            html.Div(
                id="widget_news",
                children=[
                    widget_dax,
                    widget_dax_news,
                ],
            ),
        ],
    )
    return content_home
