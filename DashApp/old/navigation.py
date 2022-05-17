import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


df = pd.read_csv(
    'https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [


        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Here you can Search"
        ),

        html.Div(dcc.Input(id='input-box1', placeholder='Select DAX-Company', type='text')),
        html.Div(dcc.Input(id='input-box2', placeholder='Select Time', type='text')),
        html.Button('Submit', id='button-example-1'),
        html.Div(id='output-container-button',
                 children='Enter a value and press submit'),

        dbc.Nav(
            [
                dbc.NavLink("KPI's", href="/", active="exact"),
                dbc.NavLink("Stocks", href="/page-1", active="exact"),
                dbc.NavLink("News", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
            html.H4(
            "Quote of the Day:"
            ),
            html.P(
            "Every new day begins with possibilities"
            ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button-example-1', 'n_clicks')],
    [dash.dependencies.State('input-box1', 'value')])

def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(debug=True)