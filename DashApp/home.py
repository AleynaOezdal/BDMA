import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import pandas_datareader.data as web
import requests as req
from setup import create_company_dict
import dash_bootstrap_components as dbc


company_dict = create_company_dict()

#wie erscheint direkt die Seite, ohne

def api_call_date_time(data, date, time):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{date}/{time}"
    result = req.get(url)
    return result.json()





def get_home_content(date, time):

    content_header_home = html.Div(
        id="content_header_kpi",
        children=[
            html.H3(
                id="content_header_first", children=["Willkommen auf unserem Dashboard"]
            ),
        ],
    )

    #Dax-Chart
    

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
                    widget_dax_news,
                    # widget_two_news,
                ],
            ),
        ],
    )
    return content_home
