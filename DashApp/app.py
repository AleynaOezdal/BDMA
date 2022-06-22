from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import home
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
def overview(value, date, time):
    overview_content = html.Div(
        id="content",
        children=[
            kpi.get_value_without_kpi(value), 
            html.Div(id="widget", children=[

        ])],
    )
    return overview_content

#home
# home_content = html.Div(id="side_version", children=[])

app.layout = html.Div(
    children=[
        header,
        html.Div(id="side", children=[
            dcc.Location(id="url"), 
            sb.sidebar,
            content]),
    ]
)

@app.callback(
    Output("page_content", "children"),
    Input("url", "pathname"),
    Input('dropdown', 'value'),
    Input('single_date_picker', 'date'),
    Input('dropdown_time', 'value')
)

# side posiblilitis
def render_page_content(pathname, value, date, time):
    if pathname == "/":
        return [overview(value, date, time)]
    elif pathname == "/Keyperformance":  # navigationpointone
        return [kpi.get_kpi_content_value(value)]
    elif pathname == "/Investorrelations":  # navigationpointtwo
        return [Investorrelations.get_stocks_content_value(value)]
    elif pathname == "/Companyenvironment":  # navigationpointthree
        return [news.get_news_content(value, date, time)]
    # If the user tries to reach a different page, return a 404 message
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ])


if __name__ == "__main__":
    app.run_server(debug=True)
