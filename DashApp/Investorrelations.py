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
        widget_one_stocks = html.Div(id = 'stocks_widget_2', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="Adidas")
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dcc.Graph(
                                id="output-graph",
                                style={"width": "20vmax", "height": "10vmax"},
                            )
                            ],     style={"width": "50%", "margin": "5%"})

                        ],)

        #widget-two-stocks
        widget_two_stocks = html.Div(id = 'stocks_widget_2', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="DAX40")
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dcc.Graph(
                                id="output-graph",
                                style={"width": "20vmax", "height": "10vmax"},
                            )
                            ],     style={"width": "50%", "margin": "5%"})

                        ],)

        #widget-three-stocks
        d = {
            '': ['Price', 'Change','Open', 'Day Before','Highest', 'Lowest','Marketcap', 'Date'], 
            ' ': ['234,32', '4,5','235,23', '115,23','232,24', '114,12','35,5 MRD.', '30.05.2022']}
        df = pd.DataFrame(data=d)

        widget_three_stocks = html.Div(id = 'stocks_widget', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="Key Characteristics")
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dbc.Table.from_dataframe(df)
                            ])

                        ],)

        #widget-four-stocks
        # get widget data Dividends
        gross_profit_api_data = api_call("gross_profit", company_dict[value])
        gross_profit_api_data_df = pd.DataFrame(
            gross_profit_api_data, index=["Gross Profit"]
        ).T
        if (
                gross_profit_api_data_df["Gross Profit"][0] != 0
                and gross_profit_api_data_df["Gross Profit"][0] != "NaN"
        ):
            gross_profit = short_num(gross_profit_api_data_df["Gross Profit"][0])
        else:
            gross_profit = 0

        gross_profit_df = gross_profit_api_data_df.sort_index()

        # figure dividends bar chart
        fig_dividends = go.Figure(
            data=[go.Pie(labels = ['Insiders', 'Institutionen mit Aktienbeteiligung', 'Streubesitz Institutionen']
,
            values=[4500, 2500, 1053, 500])])

        # style of the figure total revenue
        colors = ['gold', 'mediumturquoise', 'darkorange']

        fig_dividends.update_traces(hoverinfo='label', textinfo='value', textfont_size=10,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2))
        )

        fig_dividends.update_layout(
            showlegend=True,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            uniformtext_minsize=5,
        )

        # widget-four-stocks
        widget_four_stocks = html.Div(id='stocks_widget', children=[
            html.Div(
                id="stocks_widget_text",
                children=[
                    html.P(id="stocks_widget_header", children="Major Holders")
                ], ),
            html.Div(id='stocks_graph', children=[
                dcc.Graph(
                    figure=fig_dividends,
                    style={"width": "20vmax", "height": "10vmax"},
                )
            ], )

        ], )


        # get widget data Dividends
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

        # figure dividends bar chart
        fig_dax_data_per_day = go.Figure(
            go.Bar(
                y=total_revenue_df["Total Revenue"],
                x=total_revenue_df.index,
                text=total_revenue_df["Total Revenue"],
            )
        )
        # style of the figure total revenue
        fig_dax_data_per_day.update_traces(
            marker_color="#79EB71", textposition="inside", texttemplate="%{text:.3s}"
        )

        fig_dax_data_per_day.update_layout(
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
                    html.P(id="stocks_widget_header", children="Dividendenzahlungen")
                ], ),
            html.Div(id='stocks_graph', children=[
                dcc.Graph(
                    figure=fig_dax_data_per_day,
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