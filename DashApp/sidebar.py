from dash import dcc, html
import dash_bootstrap_components as dbc
from datetime import date

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

#navigation/sidebar
sidebar = html.Div(id = 'navigation',children=[
            html.P(
                'Here you can Search'
            ),

            html.Div(dcc.Input(id='input-box1', placeholder='Select DAX-Company', type='text')),
            #absatz
            html.Br(),
            dcc.DatePickerSingle(
                date=date(2022, 5, 17),
                display_format='DD MM YY'
            ),
            html.Br(),
            html.Button('Submit', id='button-example-1'),
            html.Div(id='output-container-button',
                    children='Enter a value and press submit'),
            html.Br(),
            dbc.Nav(
                [
                    dbc.NavLink("KPI's", href="/KPI's", active='exact'),
                    dbc.NavLink('Stocks', href='/Stocks', active='exact'),
                    dbc.NavLink('News', href='/News', active='exact'),
                ],
                vertical=True,
                pills=True,
            ),
                html.H4(
                'Quote of the Day:'
                ),
                html.P(
                'Every new day begins with possibilities'
                ),
        ], style = {'width': '20%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'top': 0, 'left': 0, 'bottom': 0, 'padding': '2rem 1rem'})
