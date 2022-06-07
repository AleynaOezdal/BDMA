from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from company_map import *
from setup import create_company_dict

# get all dax companys

company_dict = create_company_dict()
data_kpi = []
for entry in company_dict:
    if entry in dict_company_names:
        name = dict_company_names[entry]
    else:
        name = entry.title()

    if "_" in name:
        name = name.replace("_", " ")
    data_kpi.append(name)

# navigation/sidebar
sidebar = html.Div(
    id="navigation",
    children=[
        html.Br(),
        dcc.Dropdown(
            data_kpi,
            placeholder="DAX-Company auswählen",
            value="None",
            id="dropdown",  # dropdown to select company
        ),
        # absatz
        html.Br(),
        html.Div(
            id="date_picker",
            children=[
                dcc.DatePickerSingle(
                    placeholder="Datum auswählen",
                    display_format="DD MM YY",  # datepicker to select date
                ),
            ],
        ),
        html.Br(),
        html.Button("Suchen", id="button_search"),  # button to submit
        dbc.Nav(
            [
                html.Br(),  # section
                # route of the navigation points
                dbc.NavLink(
                    "Key Performance",
                    href="/Keyperformance",
                    active="exact",
                    id="navigation_point_one",
                ),
                html.Br(),  # section
                dbc.NavLink(
                    "Investor Relations",
                    href="/Investorrelations",
                    active="exact",
                    id="navigation_point_two",
                ),
                html.Br(),
                dbc.NavLink(
                    "Company Environment",
                    href="/Companyenvironment",
                    active="exact",
                    id="navigation_point_three",
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Br(),
        html.Br(),
        html.Div(
            id="quote_sidebar",
            children=[
                html.H6("Motivation des Tages:"),  # quote
                html.P('"Jeder Tag beginnt mit neuen Chancen!"'),
            ],
        ),
    ],
)
