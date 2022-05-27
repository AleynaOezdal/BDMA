from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from retrieve_sample_data import get_kpi_data

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif',
    'monaco' : 'Monaco, sans-serif'
}

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
            html.Div(children=[
                html.H5(
                    'Quote of the Day:'
                ),
                html.P(
                'Every new day begins with possibilities.'
                ),
            ], style={'font-family': font['monaco'], 'text-align':'center'})           
        ], style = {'width': '20%','height':'200%', 'vertical-align': 'middle', 'align-items': 'stretch', 'background': colors['background'], 'top': 0, 'left': 0, 'bottom': 0, 'padding': '1%'})
