from dash import html
from dash import dcc

#navigationpointtwo
#tbc in task 2

dashboard = html.Div(
    [
        html.Br(),
        html.Div(id="my-output"),
        dcc.Graph(id="output-graph"),
    ]
)
