from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from producersetup import create_company_dict

#get all dax companys

company_dict = create_company_dict()
data_kpi = []
for entry in company_dict:
    name = entry.title()
    if '_' in name:
        name = name.replace('_', ' ')
    if 'Bmw' in name:
        name = name.replace('Bmw', 'BMW')
    data_kpi.append(name)

#navigation/sidebar
sidebar = html.Div(id = 'navigation',children=[
            dcc.Dropdown(data_kpi, placeholder='DAX-Company auswählen', value = 'None', id='dropdown'),
            #absatz
            html.Br(),
            html.Div(id='date_picker', children=[
                    dcc.DatePickerSingle(
                    placeholder='Datum auswählen',
                    display_format='DD MM YY'
                ),
            ]),
            html.Br(),
            html.Button('Suchen', id='button_search'),
            dbc.Nav(
                [
                    html.Br(),
                    dbc.NavLink("Key Performance", href="/Keyperformance", active='exact', id = 'navigation_point_one'),
                    html.Br(),
                    dbc.NavLink('Investor Relations', href='/Investorrelations', active='exact', id = 'navigation_point_two'),
                    html.Br(),
                    dbc.NavLink('Company Experience', href='/Companyexperience', active='exact', id = 'navigation_point_three'),
                ],
                vertical=True,
                pills=True,
            ),
            html.Br(),
            html.Br(),
            html.Div(id = 'quote_sidebar',children=[
                html.H6(
                    'Motivation des Tages:'
                ),
                html.P(
                '"Jeder Tag beginnt mit neuen Chancen!"'
                ),
            ])
        ])
