from pkgutil import get_data
from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from company_map import *
from setup import create_company_dict
import random

def get_data_kpi():
    data_kpi = []
    for entry in create_company_dict():
        if entry in dict_company_names:
            name = dict_company_names[entry]
        else:
            name = entry.title()

        if "_" in name:
            name = name.replace("_", " ")
        data_kpi.append(name)

    return data_kpi

def get_sidebar():
    data_kpi = get_data_kpi()

    # zitate für Motivation des Tages

    zitate = [
        '"Jeder Tag beginnt mit neuen Chancen!"',
        "„Tue heute etwas, worauf du morgen stolz sein kannst.“",
        "„Die Tat unterscheidet das Ziel vom Traum.“",
        "„Niemand, der sein Bestes gegeben hat, hat es später bereut.“",
        "„Es gibt nur zwei Tage im Leben, an denen du nichts ändern kannst: Der eine ist gestern und der andere ist morgen.“",
        "„Wünsche dir nicht, dass es einfach wäre. Wünsche dir, dass du besser darin wirst.“",
        "„Scheitern ist nicht das Gegenteil von Erfolg. Es ist ein Teil davon.“",
    ]

    def selectRandom(zitate):
        return random.choice(zitate)

    # navigation/sidebar
    sidebar_content = html.Div(
        id="navigation",
        children=[
            dcc.Store(id='memory_value'),
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
                        id='date_picker_data',
                        placeholder="Datum auswählen",
                        display_format="YYYY-MM-DD",  # datepicker to select date
                    ),
                ],
            ),
            html.Br(),
            dbc.Nav(
                [
                    dbc.NavLink(
                        "Startseite",
                        href="/Home",
                        active="exact",
                        id="navigation_point_home",
                    ),
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
                    html.P(random.choice(zitate)),
                ],
            ),
        ],
    )
    return sidebar_content
