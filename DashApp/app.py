from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sidebar as sb
import kpi
import news
import Investorrelations
from datetime import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# datetime object containing current date and time
now = datetime.now()

dt_string = now.strftime("%H")

# if-elif to use the right greeting on time

if int(dt_string) >= 0 and int(dt_string) <= 9:
    greeting = "Guten Morgen "
elif int(dt_string) >= 10 and int(dt_string) <= 17:
    greeting = "Guten Tag "
elif int(dt_string) >= 18 and int(dt_string) <= 23:
    greeting = "Guten Abend "

# header
header = html.Div(
    id="Header",
    children=[
        html.H2(children="DAX40 - das Unternehmer Dashboard"),
        html.Div(children=[greeting + "!"]),
        html.Div(
            id="second_header",
            children="Team DAX40 wünscht Ihnen einen erfolgreichen Tag mit richtigen Entscheidungen!",
        ),
    ],
)

# content
content = html.Div(id="page_content", children=[])

# overview
def overview(value):
    overview_content = html.Div(
        id="content",
        children=[kpi.get_value_without_kpi(value), html.Div(id="widget", children=[])],
    )
    return overview_content


# app layout
app.layout = html.Div(
    children=[
        header,
        html.Div(id="side", children=[dcc.Location(id="url"), sb.sidebar, content]),
    ]
)


@app.callback(
    Output("page_content", "children"),
    Input("url", "pathname"),
    Input("button_search", "n_clicks"),
    State("dropdown", "value"),
)

# side posiblilitis
def render_page_content(pathname, n_clicks, value):
    if n_clicks is None:
        return [overview(value)]
    else:
        if pathname == "/":
            return [overview(value)]
        elif pathname == "/Keyperformance":  # navigationpointone
            return [kpi.get_kpi_content_value(value)]
        elif pathname == "/Investorrelations":  # navigationpointtwo
            return [html.Div(
                    id="content_news",
                    children=[
                        Investorrelations.get_stocks_content_value(value),
                        html.Div(
                            id="widget_news",
                            children=[
                                Investorrelations.widget_one_stocks,
                            ],
                        ),
                    ],
                    style={
                        "width": "100%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                        "font-family": "Arial, Helvetica, sans-serif",
                    },
                )]
        elif pathname == "/Companyenvironment":  # navigationpointthree
            return [news.get_news_content(value)]
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)
