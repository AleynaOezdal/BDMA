from webbrowser import get
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
from company_map import *
from setup import create_company_dict, timezone
import random
import dash_mantine_components as dmc

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

# zitate für Motivation des Tages

zitate = [    '"Jeder Tag beginnt mit neuen Chancen!"',
                  '„Tue heute etwas, worauf du morgen stolz sein kannst.“',
                  '„Die Tat unterscheidet das Ziel vom Traum.“',
                  '„Niemand, der sein Bestes gegeben hat, hat es später bereut.“',
                  '„Es gibt nur zwei Tage im Leben, an denen du nichts ändern kannst: Der eine ist gestern und der andere ist morgen.“',
                  '„Wünsche dir nicht, dass es einfach wäre. Wünsche dir, dass du besser darin wirst.“',
                  '„Scheitern ist nicht das Gegenteil von Erfolg. Es ist ein Teil davon.“'
            ]

def selectRandom(zitate):
    return random.choice(zitate)


# navigation/sidebar
sidebar = html.Div(
    id="navigation",
    children=[
        html.Br(),
        dcc.Dropdown(
            data_kpi,
            placeholder="DAX-Company auswählen",
            value="Adidas",
            id="dropdown",  # dropdown to select company
        ),
        # absatz
        html.Br(),
        html.Div(
            id="date_picker",
            children=[
                dcc.DatePickerSingle(
                    id='single_date_picker',
                    placeholder=datetime.today(),
                    date = datetime.today().strftime("%Y-%m-%d"),
                    display_format="DD.MM.YYYY",

                ),
            ],
        ),
        html.Br(),
        dcc.Dropdown(
            timezone,
            placeholder= datetime.now().strftime("%H:") +"00",
            value= datetime.now().strftime("%H:") +"00",
            id="dropdown_time", # dropdown to select company
        ),
        dbc.Nav(
            [
                html.Br(),  # section
                # route of the navigation points
                dbc.NavLink(
                    "Startseite",
                    href="/",
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
