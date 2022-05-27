from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from retrieve_sample_data import get_kpi_data

#get all dax companys
data_kpi = ['adidas', 'deutsche post']
# for entry in get_kpi_data():
#     if 'level' in entry:
#         data_kpi.append(entry['_id'])

data_kpi.sort()

#navigation/sidebar
sidebar = html.Div(id = 'navigation',children=[
            html.P(
                'Here you can Search'
            ),
            #html.Div(dcc.Input(id='input-box1', placeholder='Select DAX-Company', type='text')),
            dcc.Dropdown(data_kpi, placeholder='Select DAX-Company', value = 'None', id='demo-dropdown'),
            html.Div(id='dd-output-container'),
            #absatz
            html.Br(),
            dcc.DatePickerSingle(
                date=date(2022, 5, 17),
                display_format='DD MM YY'
            ),
            html.Div(id='output-container-button',
                    children=''),
            html.Br(),
            html.Button('Submit', id='button-example-1'),
            dbc.Nav(
                [
                    dbc.NavLink("KPI's", href="/KPI's", active='exact'),
                    dbc.NavLink('Stocks', href='/Stocks', active='exact'),
                    dbc.NavLink('News', href='/News', active='exact'),
                ],
                vertical=True,
                pills=True,
            ),
            html.Div(id = 'quote_sidebar',children=[
                html.H5(
                    'Quote of the Day:'
                ),
                html.P(
                'Every new day begins with possibilities.'
                ),
            ])           
        ])
