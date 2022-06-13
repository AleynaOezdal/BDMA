
import pandas as pd
from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req
from dash import dcc, html
import plotly.express as px
import pandas as pd

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

company_dict = create_company_dict()


def api_call(data, value):
    url = f"http://127.0.0.1:5000/{data}/{value}"
    result = req.get(url)
    return result.json()

def get_news_content_value(value):
    if value in data_kpi:
        # value for header
        name = value

        # small letter for dict
        if " " in value:
            value = value.replace(" ", "_")
        if "." in value:
            value = value.replace(".", "")

        value = value.lower()

        wkns_and_isins = api_call("wkns_and_isins", value)

        #content-header-news
        content_header_news = html.Div(
            id="content_header_news",
            children=[
                html.H3(
                    id="content_header_first", children=["Company Relations "]),
                html.H3(id="content_header_second", children=["for"]),
                html.H3(
                    id="content_header_third", children=[name + " " + wkns_and_isins]
                ),
            ],
        )

        return content_header_news

# widget-one-news
widget_one_news = html.Div(
    id="news_widget",
    children=[
        html.Div(
            children=[
                html.H4(id="news_widget_header", children="NEWS"),
                html.P(id="news_widget_text", children="finanzen.net"),
                html.P(
                    id="kpi_widget_pos",
                    children=["▲"],
                    style={"color": "green", "font-size": "80%"},
                ),
            ],
            style={"width": "50%", "margin": "5%"},
        )
    ],
)

# widget-two-news
widget_two_news = html.Div(
    id="news_widget",
    children=[
        html.Div(
            children=[
                html.H5(id="news_widget_header", children="MITARBEITER-REVIEWS"),
                html.P(id="news_widget_text", children="kununu"),
                html.P(
                    id="news_widget_pos",
                    children=["▲"],
                    style={"color": "green", "font-size": "80%"},
                ),
            ],
            style={"width": "50%", "margin": "5%"},
        )
    ],
)


widget_three_news = html.Div(
    id="news_widget",
    children=[
        html.Div(
            children=[
                html.P(id="news_widget_header", children="ALLE WELT NEWS"),
                html.P(id="news_widget_text", children="boerse.de"),
                html.P(
                    id="news_widget_pos",
                    children=["▲"],
                    style={"color": "green", "font-size": "80%"},
                ),
            ],
            style={"width": "50%", "margin": "5%"},
        )
    ],
)

# widget-four-news
widget_four_news = html.Div(
    id="news_widget",
    children=[
        html.Div(
            children=[
                html.P(id="news_widget_header", children="BÖRSENNEWS-FORUM"),
                html.P(id="news_widget_text", children="boersennews.de/{ISIN}"),
                html.P(
                    id="news_widget_pos",
                    children=["▲"],
                    style={"color": "green", "font-size": "80%"},
                ),
            ],
            style={"width": "50%", "margin": "5%"},
        )
    ],
)

# widget-five-news
widget_five_news = html.Div(
    id="news_widget",
    children=[
        html.Div(
            children=[
                html.P(id="news_widget_header", children="DAX NEWS"),
                html.P(id="news_widget_text", children="finanzen.net"),
                html.P(
                    id="news_widget_pos",
                    children=["▲"],
                    style={"color": "green", "font-size": "80%"},
                ),
            ],
            style={"width": "50%", "margin": "5%"},
        )
    ],
)

# widget-six-news
widget_six_news = html.Div(
    id="news_widget",
    children=[
        html.Div(
            children=[
                html.P(id="news_widget_header", children="KUNDEN"),
                html.P(id="news_widget_text", children="Trustpilot"),
                html.P(
                    id="news_widget_pos",
                    children=["▲"],
                    style={"color": "green", "font-size": "80%"},
                ),
            ],
            style={"width": "50%", "margin": "5%"},
        )
    ],
)
