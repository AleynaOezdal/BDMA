from dash import html
from datetime import datetime


def get_header():
    # datetime object containing current date and time
    now = datetime.now()

    dt_string = now.strftime("%H")

    # if-elif to use the right greeting on time

    if int(dt_string) >= 0 and int(dt_string) <= 9:
        greeting = "Guten Morgen "
    elif int(dt_string) >= 10 and int(dt_string) <= 17:
        greeting = "Guten Tag "
    elif int(dt_string) >= 18 and int(dt_string) <= 23:
        greeting = "Guten Abend "

    # header
    header_content = html.Div(
        id="Header",
        children=[
            html.H2(children="DAX40 - das Unternehmer Dashboard"),
            html.Div(children=[greeting + "!"]),
            html.Div(
                id="second_header",
                children="Team DAX40 wünscht Ihnen einen erfolgreichen Tag mit richtigen Entscheidungen!",
            ),
        ],
    )
    return header_content
