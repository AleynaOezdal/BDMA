from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

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

# get short numbers with two decimal places
def short_num(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return "%.2f%s" % (
        num,
        ["", " Tausend", " MIO.", " MRD.", " BIO.", " Trillionen"][magnitude],
    )

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
                            ],     style={"width": "50%", "margin": "5%"})

                        ],)

        #widget-two-stocks
        widget_two_stocks = html.Div(id = 'stocks_widget', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="Key Characteristics"),
                                #html.P(id="stocks_widget_key", children=ebit),
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dcc.Graph(
                                id="output-graph",
                                style={"width": "20vmax", "height": "10vmax"},
                            )
                            ],     style={"width": "50%", "margin": "5%"})

                        ],)

        #widget-three-stocks
        widget_three_stocks = html.Div(id = 'stocks_widget', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="Dividendenzahlungen"),
                                #html.P(id="stocks_widget_key", children=ebit),
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dcc.Graph(
                                id="output-graph",
                                style={"width": "20vmax", "height": "10vmax"},
                            )
                            ],      style={"width": "50%", "margin": "5%"})

                        ],)

        #widget-four-stocks
        widget_four_stocks = html.Div(id = 'stocks_widget', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="DAX40"),
                                #html.P(id="stocks_widget_key", children=ebit),
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dcc.Graph(
                                id="output-graph",
                                style={"width": "20vmax", "height": "10vmax"},
                            )
                            ],     style={"width": "50%", "margin": "5%"})

                        ],)


        # get widget data major holders
        total_revenue_api_data = api_call("total_revenue", company_dict[value])
        total_revenue_api_data_df = pd.DataFrame(
            total_revenue_api_data, index=["Total Revenue"]
        ).T

        if (
                total_revenue_api_data_df["Total Revenue"][0] != 0
                and total_revenue_api_data_df["Total Revenue"][0] != "NaN"
        ):
            revenue = short_num(total_revenue_api_data_df["Total Revenue"][0])
        else:
            revenue = 0

        total_revenue_df = total_revenue_api_data_df.sort_index()

        # figure total revenue bar chart
        fig_major_holders = go.Figure(
            go.Bar(
                y=total_revenue_df["Total Revenue"],
                x=total_revenue_df.index,
                text=total_revenue_df["Total Revenue"],
            )
        )
        # style of the figure total revenue
        fig_major_holders.update_traces(
            marker_color="#79EB71", textposition="inside", texttemplate="%{text:.3s}"
        )

        fig_major_holders.update_layout(
            showlegend=False,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#F6F6F6",
            plot_bgcolor="#F6F6F6",
            uniformtext_minsize=6,
        )

        # widget-four-stocks
        widget_five_stocks = html.Div(id='stocks_widget', children=[
            html.Div(
                id="stocks_widget_text",
                children=[
                    html.P(id="stocks_widget_header", children="Major Holders"),
                    # html.P(id="stocks_widget_key", children=ebit),
                ], ),
            html.Div(id='stocks_graph', children=[
                dcc.Graph(
                    figure=fig_major_holders,
                    style={"width": "20vmax", "height": "10vmax"},
                )
            ], )

        ], )

        content = html.Div(
            id="content_stocks",
            children=[
                content_header_stocks,
                html.Div(
                    id="widget",
                    children=[
                        widget_one_stocks,
                        widget_two_stocks,
                        widget_three_stocks,
                        widget_four_stocks,
                        widget_five_stocks,
                    ],
                ),
            ],
        )

        return content

    else:
        content_header_stocks = html.H3(id="content-header", children=["Select a Company"])
        return content_header_stocks