from dash import dcc, html
import pandas as pd
from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req

#example DataFrame

d = {'message': ['Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster'], 'date': ['23:52', '11:50'], 'class': ['Negative', 'Positive']}
df = pd.DataFrame(data=d)

company_dict = create_company_dict()

def api_call(data, value):
    url = f"http://127.0.0.1:5000/{data}/{value}"
    result = req.get(url)
    return result.json()

# get short numbers with two decimal places
def short_num(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return "%.2f%s" % (
        num,
        ["", " Tausend", " MIO.", " MRD.", " BIO.", " Trillionen"][magnitude],
    )


# value to select a company and navigationpoint
def get_value_without_kpi(value):
    if value == "None":
        content = html.H3(
            id="content-header", children=["Wählen Sie ein Unternehmen aus"]
        )
        return content
    else:
        content = html.H3(
            id="content-header", children=["Wählen Sie ein Navigationspunkt aus"]
        )
        return content

def get_news_content(value):
    if value in data_kpi:
        # value for header
        name = value

        # small letter for dict
        if " " in value:
            value = value.replace(" ", "_")
        if "." in value:
            value = value.replace(".", "")

        value = value.lower()

        wkns_and_isins = api_call("wkns_and_isins", value)

        # content-header-kpi
        content_header_news = html.Div(
            id="content_header_news",
            children=[
                html.H3(
                    id="content_header_first", children=["Company Environment "]
                ),
                html.H3(id="content_header_second", children=["for"]),
                html.H3(id="content_header_third", children=[name + " " + wkns_and_isins]),
            ],
        )

        # widget-one-news
        widget_one_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    children=[
                        html.H6(id="news_widget_header", children="Unternehmensnews"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(df)
                        ]),     
                    ],
                    style={"width": "50%", "margin": "5%"},
                )
            ],
        )

        # widget-one-news
        widget_two_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    children=[
                        html.H6(id="news_widget_header", children="Mitarbeiter-Bewertungen"),
                        html.Div(children=[
                            html.Div(id ='news_latest_positive', children=[
                                html.P(children='Latest Positive')
                            ]),
                            html.Div(id ='news_latest_negative',children=[
                                html.P(children='Latest Negative')
                            ])
                        ]),     
                    ],
                    style={"width": "50%", "margin": "5%"},
                )
            ],
        )

        content_news =html.Div(
                id="content_news",
                children=[
                    content_header_news,
                    html.Div(
                        id="widget_news",
                        children=[
                            widget_one_news,
                            widget_two_news,
                            widget_one_news,
                            widget_one_news,
                            widget_one_news,
                            widget_one_news,
                        ],
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "inline-block",
                    "vertical-align": "middle",
                    "font-family": "Arial, Helvetica, sans-serif",
                },
            )

        return content_news
    else:
        content_header_news = html.H3(id="content-header", children=["Select a Company"])
        return content_header_news

# # widget-one-news
# widget_one_news = html.Div(
#     id="news_widget",
#     children=[
#         html.Div(
#             children=[
#                 html.H4(id="news_widget_header", children="NEWS"),
#                 html.P(id="news_widget_text", children="finanzen.net"),
#                 html.P(
#                     id="kpi_widget_pos",
#                     children=["▲"],
#                     style={"color": "green", "font-size": "80%"},
#                 ),
#             ],
#             style={"width": "50%", "margin": "5%"},
#         )
#     ],
# )

# # widget-two-news
# widget_two_news = html.Div(
#     id="news_widget",
#     children=[
#         html.Div(
#             children=[
#                 html.H5(id="news_widget_header", children="MITARBEITER-REVIEWS"),
#                 html.P(id="news_widget_text", children="kununu"),
#                 html.P(
#                     id="news_widget_pos",
#                     children=["▲"],
#                     style={"color": "green", "font-size": "80%"},
#                 ),
#             ],
#             style={"width": "50%", "margin": "5%"},
#         )
#     ],
# )


# widget_three_news = html.Div(
#     id="news_widget",
#     children=[
#         html.Div(
#             children=[
#                 html.P(id="news_widget_header", children="ALLE WELT NEWS"),
#                 html.P(id="news_widget_text", children="boerse.de"),
#                 html.P(
#                     id="news_widget_pos",
#                     children=["▲"],
#                     style={"color": "green", "font-size": "80%"},
#                 ),
#             ],
#             style={"width": "50%", "margin": "5%"},
#         )
#     ],
# )

# # widget-four-news
# widget_four_news = html.Div(
#     id="news_widget",
#     children=[
#         html.Div(
#             children=[
#                 html.P(id="news_widget_header", children="BÖRSENNEWS-FORUM"),
#                 html.P(id="news_widget_text", children="boersennews.de/{ISIN}"),
#                 html.P(
#                     id="news_widget_pos",
#                     children=["▲"],
#                     style={"color": "green", "font-size": "80%"},
#                 ),
#             ],
#             style={"width": "50%", "margin": "5%"},
#         )
#     ],
# )

# # widget-five-news
# widget_five_news = html.Div(
#     id="news_widget",
#     children=[
#         html.Div(
#             children=[
#                 html.P(id="news_widget_header", children="DAX NEWS"),
#                 html.P(id="news_widget_text", children="finanzen.net"),
#                 html.P(
#                     id="news_widget_pos",
#                     children=["▲"],
#                     style={"color": "green", "font-size": "80%"},
#                 ),
#             ],
#             style={"width": "50%", "margin": "5%"},
#         )
#     ],
# )

# # widget-six-news
# widget_six_news = html.Div(
#     id="news_widget",
#     children=[
#         html.Div(
#             children=[
#                 html.P(id="news_widget_header", children="KUNDEN"),
#                 html.P(id="news_widget_text", children="Trustpilot"),
#                 html.P(
#                     id="news_widget_pos",
#                     children=["▲"],
#                     style={"color": "green", "font-size": "80%"},
#                 ),
#             ],
#             style={"width": "50%", "margin": "5%"},
#         )
#     ],
# )
