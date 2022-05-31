from dash import html
from dash import dcc

dashboard = html.Div([
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(id="output-graph"),
])
