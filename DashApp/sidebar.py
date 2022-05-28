from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from company_dic import *

#get all dax companys
data_kpi = []
for entry in company_dict:
    data_kpi.append(entry)

#navigation/sidebar
sidebar = html.Div(id = 'navigation',children=[
            html.P(
                'Here you can Search'
            ),
            #html.Div(dcc.Input(id='input-box1', placeholder='Select DAX-Company', type='text')),
            dcc.Dropdown(data_kpi, placeholder='DAX-Company auswählen', value = 'None', id='dropdown'),
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
            html.Button('Suchen', id='button_search'),
            html.Br(),
            dbc.Nav(
                [
                    html.Br(),
                    dbc.NavLink("KPI's", href="/KPI's", active='exact', id = 'navigation_point_one'),
                    html.Br(),
                    dbc.NavLink('Investor Relations', href='/Investorrelations', active='exact', id = 'navigation_point_two'),
                    html.Br(),
                    dbc.NavLink('Company Experience', href='/Companyexperience', active='exact', id = 'navigation_point_three'),
                ],
                vertical=True,
                pills=True,
            ),
            html.Br(),
            html.Div(id = 'quote_sidebar',children=[
                html.H5(
                    'Motivation des Tages:'
                ),
                html.P(
                'Jeder Tag beginnt mit neuen Chancen!'
                ),
            ])           
        ])
