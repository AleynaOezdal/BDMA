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

def get_stocks_content_value(value):
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

        #content-header-stocks
        content_header_stocks = html.Div(
            id="content_header_stocks",
            children=[
                html.H3(
                    id="content_header_first", children=["Investor Relations "]),
                html.H3(id="content_header_second", children=["for"]),
                html.H3(
                    id="content_header_third", children=[name + " " + wkns_and_isins]
                ),
            ],
        )


#widget-one-stocks
widget_one_stocks = html.Div(id = 'stocks_widget', children=[
                html.Div(
                    id="stocks_widget_text",
                    children=[
                        html.P(id="stocks_widget_header", children="Adidas"),
                        #html.P(id="stocks_widget_key", children=ebit),
                    ],),
                    html.Div(id = 'stocks_graph', children= [
                        dcc.Graph(
                        id="output-graph",
                        style={"width": "20vmax", "height": "10vmax"},
                    )
                    ],)

                ],)







#dashboard = html.Div(
#    [
#        html.Br(),
 #       html.Div(id="my-output"),
  #      dcc.Graph(id="output-graph"),
   # ]
#)
