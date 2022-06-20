import dash
from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# import home
from sidebar import get_sidebar
from header import get_header
# import kpi
# import news
# import Investorrelations
from datetime import datetime

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

app.layout = html.Div(
                children=[
                    get_header(),
                    html.Div(id="side", children=[
                        get_sidebar(),
                        dash.page_container]),
                ]
            )

@app.callback(
    Output('memory_value', 'value'),
    Input('dropdown','value'),
    prevent_initial_call=True
)

def get_value(value):
    return value

if __name__ == '__main__':
	app.run_server(debug=True)
