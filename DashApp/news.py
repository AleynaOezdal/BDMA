from dash import dcc, html
import pandas as pd
from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req

#example DataFrame

d = {
    '': ['Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster'], 
    'Datum': ['23:52', '11:50','23:52', '11:50','23:52', '11:50'], 
    'Klassifizierung': ['Negative', 'Positive','Negative', 'Positive','Negative', 'Positive']}
df = pd.DataFrame(data=d)

d_2 = {
    '': ['Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster'],  
    'Klassifizierung': ['Negative', 'Positive','Negative', 'Positive','Negative', 'Positive']}
df_2 = pd.DataFrame(data=d_2)

d_3 = {
    '': ['Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster'], 
    'Datum': ['23:52', '11:50','23:52', '11:50','23:52', '11:50']}
df_3 = pd.DataFrame(data=d_3)

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
        company_news = api_call('community_news', value)
        company_news_df = pd.DataFrame(company_news)
        company_news_df_2 = pd.DataFrame()

        company_news_df_2[''] = company_news_df['message'][0:6]
        company_news_df_2['Datum'] = company_news_df['time'][0:6]
        company_news_df_2['Klassifizierung'] = company_news_df['class'][0:6]

        widget_one_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Unternehmensnews"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(df)
                            # html.Table(
                            #     # Header
                            #     [html.Tr([html.Th(col) for col in df.columns]) ] +
                            #     # Body
                            #     [html.Tr([
                            #         html.Td(df.iloc[i][col]) for col in df.columns
                            #     ]) for i in range(min(len(df), 6))]
                            # )
                        ]),     
                    ]
                )
            ],
        )

        # widget-two-news
        widget_two_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Mitarbeiter-Bewertungen"),
                        html.Div(children=[
                            html.Div(id ='news_latest_positive', children=[
                                html.P(children='Latest Positive'),
                                html.Div(id = 'news_company_review',children = [
                                    html.P(id= 'news_company_review_text', children='nike und puma es gibt sehr viele schöne…')
                                ])
                            ]),
                            html.Div(id ='news_latest_negative',children=[
                                html.P(children='Latest Negative'),
                                html.Div(id = 'news_company_review', children = [
                                    html.P(id= 'news_company_review_text', children='Nutzlosester Support aller Zeiten')
                                ])
                            ])
                        ]),     
                    ]
                )
            ],
        )

        # widget-three-news
        widget_three_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Kundenrezesionen"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(df_2)
                        ]),     
                    ]
                )
            ],
        )

        # widget-four-news
        widget_four_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="DAX-News"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(df_3)
                        ]),     
                    ]
                )
            ],
        )

        # widget-five-news
        widget_five_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Globale News"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(df_3)
                        ]),     
                    ]
                )
            ],
        )

        # widget-six-news
        widget_six_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Börsen-Community"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(df_3)
                        ]),     
                    ]
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
                            widget_three_news,
                            widget_four_news,
                            widget_five_news,
                            widget_six_news,
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
