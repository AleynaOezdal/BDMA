from unittest import skip
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req

company_dict = create_company_dict()

#config = {'displayModeBar': False}

def api_call(data, value):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{value}"
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



# value to select a company and navigationpoint
def get_value_without_kpi(value):
    if value == "None":
        content = html.H3(
            id="content-header", children=["Wählen Sie ein Unternehmen aus"]
        )
        return content
    else:
        content = html.H3(
            id="content-header", children=["Wählen Sie ein Navigationspunkt aus"]
        )
        return content


def get_kpi_content_value(value):
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

        # content-header-kpi
        content_header_kpi = html.Div(
            id="content_header_kpi",
            children=[
                html.H3(id="content_header_first", children=["Key Performance Indicators "]),
                html.H3(id="content_header_second", children=["for"]),
                html.H3(id="content_header_third", children=[name + " " + wkns_and_isins]),
            ],
        )

        # get wiget data ebit
        ebit_data = api_call("ebit", company_dict[value])
        ebit_api_data_df = pd.DataFrame(ebit_data, index=["Ebit"]).T
        if ebit_api_data_df["Ebit"][0] != 0 and ebit_api_data_df["Ebit"][0] != "NaN":
            ebit = short_num(ebit_api_data_df["Ebit"][0])
        else:
            ebit = 0

        # df to sort the index for the line chart
        ebit_df = ebit_api_data_df.sort_index()

        fig_ebit = go.Figure(go.Scatter(y=ebit_df["Ebit"], x=ebit_df.index))

        # sytle from the line chart
        fig_ebit.update_traces(mode="lines", line_color="#EA000D")

        fig_ebit.update_layout(
            showlegend=False,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#F6F6F6",
            plot_bgcolor="#F6F6F6",
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
        )
        # style the widget and grapgh
        widget_ebit_kpi = html.Div(
            id="kpi_widget",
            children=[
                html.Div(
                    id="kpi_widget_text",
                    children=[
                        html.P(id="kpi_widget_header", children="EBIT"),
                        html.P(id="kpi_widget_key", children=ebit),
                        html.Button([html.I( className="bi bi-info-circle-fill me-2")], id="info-button")
                    ],
                ),
                html.Div(
                    id="kpi_graph",
                    children=[
                        dcc.Graph(
                            figure=fig_ebit,
                            style={"width": "20vmax", "height": "10vmax"},
                        )
                    ],
                ),
            ],
        )


        # get widget data gross profit
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

        # figure bar chart gross profit
        fig_gross_profit = go.Figure(
            go.Bar(
                x=gross_profit_df["Gross Profit"],
                y=gross_profit_df.index,
                text=gross_profit_df["Gross Profit"],
                orientation="h",
            )
        )
        fig_gross_profit.update_traces(
            marker_color="#19AD50", textposition="inside", texttemplate="%{text:.3s}"
        )  # , marker_line_color='#67E98B', marker_line_width=1.5, opacity=0.6)

        fig_gross_profit.update_layout(
            showlegend=False,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#F6F6F6",
            plot_bgcolor="#F6F6F6",
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
        )

        # div to complete the widget and graph
        widget_gross_profit_kpi = html.Div(
            id="kpi_widget",
            children=[
                html.Div(
                    id="kpi_widget_text",
                    children=[
                        html.P(id="kpi_widget_header", children="Profit Margin"),
                        html.P(id="kpi_widget_key", children=gross_profit),
                        html.Button([html.I( className="bi bi-info-circle-fill me-2")], id="info-button")
                    ],
                ),
                html.Div(
                    id="kpi_graph",
                    children=[
                        dcc.Graph(
                            figure=fig_gross_profit,
                            style={"width": "20vmax", "height": "10vmax"},
                        )
                    ],
                ),
            ],
        )

        # get wiget data net income
        net_income_api_data = api_call("net_income", company_dict[value])
        net_income_api_data_df = pd.DataFrame(
            net_income_api_data, index=["Net Income"]
        ).T
        if (
            net_income_api_data_df["Net Income"][0] != 0
            and net_income_api_data_df["Net Income"][0] != "NaN"
        ):
            income = short_num(net_income_api_data_df["Net Income"][0])
        else:
            income = 0

        # df to sort the index for the line chart
        net_income_df = net_income_api_data_df.sort_index()

        # figure
        fig_net_income = go.Figure(
            go.Scatter(y=net_income_df["Net Income"], x=net_income_df.index)
        )

        fig_net_income.update_traces(mode="lines", line_color="#EDA611")

        fig_net_income.update_layout(
            showlegend=False,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#F6F6F6",
            plot_bgcolor="#F6F6F6",
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
        )

        # div to complete and style the widget and graph
        widget_net_income_kpi = html.Div(
            id="kpi_widget",
            children=[
                html.Div(
                    id="kpi_widget_text",
                    children=[
                        html.P(id="kpi_widget_header", children="Net income"),
                        html.P(id="kpi_widget_key", children=income),
                        html.Button([html.I( className="bi bi-info-circle-fill me-2")], id="info-button")
                    ],
                ),
                html.Div(
                    id="kpi_graph",
                    children=[
                        dcc.Graph(
                            figure=fig_net_income,
                            style={"width": "20vmax", "height": "10vmax"},
                        )
                    ],
                ),
            ],
        )

        # get widget data total revenue
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
        fig_total_revenue = go.Figure(
            go.Bar(
                y=total_revenue_df["Total Revenue"],
                x=total_revenue_df.index,
                text=total_revenue_df["Total Revenue"],
            )
        )
        # style of the figure total revenue
        fig_total_revenue.update_traces(
            marker_color="#79EB71", textposition="inside", texttemplate="%{text:.3s}"
        )

        fig_total_revenue.update_layout(
            showlegend=False,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#F6F6F6",
            plot_bgcolor="#F6F6F6",
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
        )

        # div to complete/style the widget and graph
        widget_total_revenue_kpi = html.Div(
            id="kpi_widget",
            children=[
                html.Div(
                    id="kpi_widget_text",
                    children=[
                        html.P(id="kpi_widget_header", children="Revenue"),
                        html.P(id="kpi_widget_key", children=revenue),
                        html.Button([html.I( className="bi bi-info-circle-fill me-2")], id="info-button")
                    ],
                ),
                html.Div(
                    id="kpi_graph",
                    children=[
                        dcc.Graph(
                            figure=fig_total_revenue,
                            style={"width": "20vmax", "height": "10vmax"},
                        )
                    ],
                ),
            ],
        )

        # get wiget data total operating expenses
        oper_exp_api_data = api_call("total_operating_expenses", company_dict[value])
        oper_exp_api_data_df = pd.DataFrame(
            oper_exp_api_data, index=["Total Operating Expenses"]
        ).T

        if (
            oper_exp_api_data_df["Total Operating Expenses"][0] != 0
            and oper_exp_api_data_df["Total Operating Expenses"][0] != "NaN"
        ):
            level = short_num(oper_exp_api_data_df["Total Operating Expenses"][0])
        else:
            level = 0

        total_operating_expenses_df = oper_exp_api_data_df.sort_index()

        fig_total_operating_expenses = go.Figure(
            go.Bar(
                x=total_operating_expenses_df["Total Operating Expenses"],
                y=total_operating_expenses_df.index,
                text=total_operating_expenses_df["Total Operating Expenses"],
                orientation="h",
            )
        )
        fig_total_operating_expenses.update_traces(
            marker_color="#3368AD", textposition="inside", texttemplate="%{text:.3s}"
        )  # , marker_line_color='#67E98B', marker_line_width=1.5, opacity=0.6)

        fig_total_operating_expenses.update_layout(
            showlegend=False,
            margin_l=0,
            margin_r=0,
            margin_t=0,
            margin_b=0,
            paper_bgcolor="#F6F6F6",
            plot_bgcolor="#F6F6F6",
            uniformtext_minsize=6,
            modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
        )

        # widget-six-kpi
        widget_total_operating_expenses_kpi = html.Div(
            id="kpi_widget",
            children=[
                html.Div(
                    id="kpi_widget_text",
                    children=[
                        html.P(
                            id="kpi_widget_header", children="Total operating expenses"
                        ),
                        html.P(id="kpi_widget_key", children=level),
                        html.Button([html.I( className="bi bi-info-circle-fill me-2")], id="info-button")
                    ],
                ),
                html.Div(
                    id="kpi_graph",
                    children=[
                        dcc.Graph(
                            figure=fig_total_operating_expenses,
                            style={"width": "20vmax", "height": "10vmax"},
                        )
                    ],
                ),
            ],
        )

        # get wiget data esg risk score
        esg_api_data = api_call("esg_score", company_dict[value])

        if esg_api_data != 0 and esg_api_data != "NaN":
            esg = esg_api_data
            if esg >= 40:
                high_average_low = (
                    "SERVER"  # different levels and colors for the esg score
                )
                color = "red"
            elif esg <= 40 and esg >= 30:
                high_average_low = "HIGH"
                color = "red"
            elif esg <= 30 and esg >= 20:
                high_average_low = "MEDIUM"
                color = "orange"
            elif esg <= 20 and esg >= 10:
                high_average_low = "LOW"
                color = "green"
            elif esg <= 10:
                high_average_low = "NEGLIGIBLE"
                color = "green"
        else:  # if no data available
            esg = 0
            high_average_low = "NONE"
            color = "green"

        # div to complete/style the widget and graph
        widget_esg_kpi = html.Div(
            id="kpi_widget",
            children=[
                html.Div(
                    id="kpi_widget_text",
                    children=[
                        html.P(id="kpi_widget_header", children="ESG Risk Score"),
                        html.P(id="kpi_widget_key", children=esg),
                        html.Button([html.I( className="bi bi-info-circle-fill me-2")], id="info-button")
                    ],
                ),
                html.Div(
                    id="kpi_graph_text",
                    children=[
                        html.P(
                            id="kpi_widget_esg",
                            children=high_average_low,
                            style={"color": color, "font-size": "2.5vmax"},
                        )
                    ],
                ),
            ],
        )
        # description of the companies
        description = api_call("description", value)
        value_long = dict_company_names_long[value]
        distribution = api_call("industry_distribution", value_long)
        main_competitor = api_call("main_competitors", value_long)
        main_competitor_string = ""

        for entry in main_competitor:
            if value_long in entry:
                pass
            else:
                if main_competitor_string == "":
                    main_competitor_string = entry
                else:
                    main_competitor_string = main_competitor_string + ", " + entry

        # text and structure of the descripton dropwdown
        accordion = html.Div(
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        id="description",
                                        children=[
                                            html.H6("Beschreibung: "),
                                            description,
                                        ],
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    html.Div(
                                        id="branche",
                                        children=[html.H6("Branche: " + distribution)],
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        "Hauptkonkurrent: " + main_competitor_string
                                    )
                                ),
                            ]
                        ),
                        title="Detaillierte Informationen zum Unternehmen",
                    ),
                ],
                flush=True,
                start_collapsed=True,
            ),
        )
        # content from the descripton

        content = html.Div(
            id="content",
            children=[
                content_header_kpi,
                accordion,
                html.Div(
                    id="widget",
                    children=[
                        widget_ebit_kpi,
                        widget_total_revenue_kpi,
                        widget_gross_profit_kpi,
                        widget_net_income_kpi,
                        widget_esg_kpi,
                        widget_total_operating_expenses_kpi,
                    ],
                ),
            ],
        )

        return content
    else:
        content_header_kpi = html.H3(id="content-header", children=["Select a Company"])
        return content_header_kpi
