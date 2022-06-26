from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from ast import literal_eval
from datetime import datetime, timedelta, date
import ast

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

company_dict = create_company_dict()


def api_call(data, value):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{value}"
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
    y = 2*((x - min) / (max - min)) - 1

    return y

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

def check_key_char(x, value):

    key_characteristics = api_call_value_date_time("key_characteristics", value, datetime.today() - timedelta(days=1), "17:30")
    df = pd.DataFrame([key_characteristics])

    key_columns = []
    key_values = []

    for col_name in df.columns:
        key_columns.append(col_name)

    for col_name2 in df.values:
        for i in col_name2:
            key_values.append(i)

    df_key_yesterday = pd.DataFrame(
        {
            "": key_columns,
            " ": key_values,
        }
    )

    if x[""].all() == 0:
        return df_key_yesterday
    else:
        return x


def get_stocks_content_value(value, date, time):
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

        result_api_call = api_call_value_date_time("stock_price", company_dict[value], date, time)
        dax_api_call = api_call_value_date_time("stock_price", "^GDAXI", date, time)

        dax_stock = pd.DataFrame()
        for package in range(len(dax_api_call)):
            data_as_df = pd.DataFrame.from_dict(
                literal_eval(dax_api_call[package]["stock_price_onehour"])
            )
            dax_stock = pd.concat([dax_stock, data_as_df], axis=0)
        dax_stock.index = pd.to_datetime(dax_stock.index, unit="ms") + timedelta(hours=2)

        actual_stock = pd.DataFrame()
        for package in range(len(result_api_call)):
            data_as_df = pd.DataFrame.from_dict(
                literal_eval(result_api_call[package]["stock_price_onehour"])
            )
            actual_stock = pd.concat([actual_stock, data_as_df], axis=0)
        actual_stock.index = pd.to_datetime(actual_stock.index, unit="ms") + timedelta(hours=2)

        candlestick_chart = go.Figure()

        candlestick_chart.add_trace(go.Scatter(x=actual_stock.index, y=actual_stock["High"], name="Linie", line=dict(color='orange')))


        candlestick_chart.add_trace(go.Candlestick(
                    x=actual_stock.index,
                    open=actual_stock["Open"],
                    high=actual_stock["High"],
                    low=actual_stock["Low"],
                    close=actual_stock["Close"],
                    name= "Kerze", visible=False
                ))

        candlestick_chart.update_xaxes(
            rangeslider_visible=False,
            rangebreaks=[
                dict(values=["2022-06-26", "2022-06-25", "2022-06-19", "2022-06-18"]),
                dict(bounds=[17.30, 9], pattern="hour"),
            ],
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=15, label="15m", step="minute", stepmode="backward"),
                        dict(count=1, label="1h", step="hour", stepmode="backward"),
                        dict(count=4, label="4h", step="hour", stepmode="backward"),
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(step="all"),
                    ],
                )
            ),
        )

        # Add dropdown
        candlestick_chart.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{"visible": [True, False]}],
                            label="Linie",
                            method="restyle"
                        ),

                        dict(
                            args=[{"visible": [False, True]}],
                            label="Kerze",
                            method="restyle"
                        ),
                    ]),
                ),
            ]
        )

        widget_one_stocks = html.Div(id='stocks_widget_2', children=[
            html.Div(
                id="stocks_widget_text",
                children=[
                    html.P(id="stocks_widget_header", children="Performance Index " + name)
                ], ),
            html.Div(id='stocks_graph_3', children=[
                dcc.Graph(
                    figure=candlestick_chart,
                ),
            ], )

        ], )

        candlestick_chart.update_layout(
            margin_l=10,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio",
                            "hoverCompareCartesian",
                            "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d",
                            "pan3d",
                            "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup",
                            "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault",
                            "resetcameralastsave",
                            "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d",
                            "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage",
                            "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom",
                            "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo",
                            "zoomOutMapbox", "zoomin", "zoomout"])

        #widget-two-stocks

        fig = go.Figure()

        normalized_stock = normalize_data(actual_stock)
        normalized_dax = normalize_data(dax_stock)

        trace1 = go.Scatter(x=normalized_stock.index, y=normalized_stock["High"], opacity=0.7, line=dict(color='orange', width=2), name=value)

        trace2 = go.Scatter(x=normalized_dax.index, y=normalized_dax["High"], opacity=0.7, line=dict(color='blue', width=2), name="DAX")

        fig.add_trace(trace1)

        fig.add_trace(trace2)

        fig.update_xaxes(
            rangeslider_visible=False,
            rangebreaks=[
                dict(values=["2022-06-26", "2022-06-25", "2022-06-19", "2022-06-18"]),
                dict(bounds=[17.30, 9], pattern="hour"),
            ],
        )

        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin_l=10,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio",
                            "hoverCompareCartesian",
                            "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d",
                            "pan3d",
                            "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup",
                            "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault",
                            "resetcameralastsave",
                            "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d",
                            "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage",
                            "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom",
                            "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo",
                            "zoomOutMapbox", "zoomin", "zoomout"])

        widget_two_stocks = html.Div(id='stocks_widget_2', children=[
            html.Div(
                id="stocks_widget_text",
                children=[
                    html.P(id="stocks_widget_header", children="DAX und " + name)
                ], ),
            html.Div(id='stocks_graph_2', children=[
                dcc.Graph(
                    figure=fig,
                ),
            ], )

        ], )

        
        #widget-three-stocks
        key_characteristics = api_call_value_date_time("key_characteristics", value, date, time)
        df = pd.DataFrame([key_characteristics])

        key_columns = []
        key_values = []

        for col_name in df.columns:
            key_columns.append(col_name)

        for col_name2 in df.values:
            for i in col_name2:
                key_values.append(i)

        df_key = pd.DataFrame(
        {
            "": key_columns,
            " ": key_values,
        }
        )



        widget_three_stocks = html.Div(id = 'stocks_widget', children=[
                        html.Div(
                            id="stocks_widget_text",
                            children=[
                                html.P(id="stocks_widget_header", children="Key Characteristics")
                            ],),
                            html.Div(id = 'stocks_graph', children= [
                                dbc.Table.from_dataframe(check_key_char(df_key, value), bordered=True, hover=True)
                            ])

                        ],)

        # widget four stocks
        dividend_api_data = api_call("dividends", company_dict[value])

        dividend_dict = ast.literal_eval(dividend_api_data)
        dividend_final_dict = {2021: [], 2020: [], 2019: [], 2018: []}
        dividend_values = list(dividend_dict.values())
        jahr = 2021
        for value in range(1, 5):
            dividend_final_dict[jahr].append(dividend_values[-value])
            jahr = jahr - 1

        dividend_api_data_df = pd.DataFrame(
            dividend_final_dict, index=["Dividend"]
        ).T

        dividend_df = dividend_api_data_df.sort_index()

        # figure dividends bar chart
        fig_dividend = go.Figure(
            go.Bar(
                y=dividend_df["Dividend"],
                x=dividend_df.index,
                text=dividend_df["Dividend"],
            )
        )
        # style of the figure total revenue
        fig_dividend.update_traces(
            marker_color="#AEDCF5", textposition="inside", texttemplate="%{text:.3s}"
        )

        fig_dividend.update_layout(
            showlegend=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio",
                            "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation",
                            "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d",
                            "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox",
                            "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale",
                            "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud",
                            "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines",
                            "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d",
                            "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin",
                            "zoomout"]
        )

        widget_four_stocks = html.Div(id='stocks_widget', children=[
            html.Div(
                id="stocks_widget_text",
                children=[
                    html.P(id="stocks_widget_header", children="Dividendenzahlungen in €")
                ], ),
            html.Div(id='stocks_graph', children=[
                dcc.Graph(
                    figure=fig_dividend,
                    style={"width": "20vmax", "height": "25vmax"},
                )
            ], )

        ], )


        # widget-five-stocks
        # get widget data Dividends
        major_holders_api_data = api_call("major_holders", "ads") #Warum funktioniert das nicht mit company_dict[value]??
        label = list(major_holders_api_data.keys())
        value = list(major_holders_api_data.values())
        label_without_percentage = []
        label_new = label[0:3]
        value_new = value[0:3]
        for i in value_new:
            label_without_percentage.append(float(i.replace("%", "").replace(",", "")))

        colors = ['#E6E0D3', '#FF918C', '#F0CB96']

        fig_holders = go.Figure(data=[go.Pie(labels=label_new, values=label_without_percentage, hole=.3)])

        fig_holders.update_traces(hoverinfo='label+percent', marker=dict(colors=colors))

        # style of the figure Major Holders


        fig_holders.update_layout(
            showlegend=True,
            legend_font_family="Arial",
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.3,
                xanchor="left",
                x=0
            ),
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            uniformtext_minsize=5,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
        )

        # widget-five-stocks
        widget_five_stocks = html.Div(id='stocks_widget', children=[
            html.Div(
                id="stocks_widget_text",
                children=[
                    html.P(id="stocks_widget_header", children="Major Holders")
                ], ),
            html.Div(id='stocks_graph', children=[
                dcc.Graph(
                    figure=fig_holders,
                    style={"width": "20vmax", "height": "20vmax" },
                ),
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