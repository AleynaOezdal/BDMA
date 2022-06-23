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
    'Datum': ['22.05.2022', '11:50','23:52', '11:50','23:52', '11:50'], 
    'Klassifizierung': ['Negative', 'Positive','Negative', 'Positive','Negative', 'Positive']}
df = pd.DataFrame(data=d)

d_3 = {
    '': ['Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster','Ziel ist die WM Vorbereitung Oktober/November. Da werden einige auch die Aktie/Trikots kaufen.', 'Real hat die CL GEWONNEN. Adidas Ausrüster'], 
    'Datum': ['22.05.2022 23:52', '11:50','23:52', '11:50','23:52', '11:50']}
df_3 = pd.DataFrame(data=d_3)

company_dict = create_company_dict()

def api_call_value(data, value):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{value}"
    result = req.get(url)
    return result.json()

def api_call_value_date_time(data, value, date, time):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{value}/{date}/{time}"
    result = req.get(url)
    return result.json()

def api_call_date_time(data, date, time):
    url = f"https://bdma-352709.ey.r.appspot.com/{data}/{date}/{time}"
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

def get_thumbs(classification):
    if classification == 'Negative':
        content = html.I(className="bi bi-hand-thumbs-down-fill")
        return content
    elif classification == 'NEGATIVE':
        content = html.I(className="bi bi-hand-thumbs-down-fill")
        return content
    elif classification == 'Positive':
        content = html.I(className="bi bi-hand-thumbs-up-fill")
        return content
    elif classification == 'POSITIVE':
        content = html.I(className="bi bi-hand-thumbs-up-fill")
        return content

def get_table_rows_first(df):
    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[0][0]),
                    html.Td(id='table_td', children=df.iloc[0][1]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[0][2])]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[1][0]),
                    html.Td(id='table_td', children=df.iloc[1][1]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[1][2])]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[2][0]),
                    html.Td(id='table_td', children=df.iloc[2][1]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[2][2])]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[3][0]),
                    html.Td(id='table_td', children=df.iloc[3][1]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[3][2])]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[4][0]),
                    html.Td(id='table_td', children=df.iloc[4][1]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[4][2])]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[5][0]),
                    html.Td(id='table_td', children=df.iloc[5][1]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[5][2])]),
                ])
    return [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5])]

def get_table_rows_secound(df):
    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[0][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[0][1])]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[1][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[1][1])]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[2][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[2][1])]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[3][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[3][1])]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[4][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[4][1])]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[5][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[5][1])]),
                ])

    table_rows6 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[6][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[7][1])]),
                ])

    table_rows7 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[7][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[7][1])]),
                ])
    
    table_rows8 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[8][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[8][1])]),
                ])

    table_rows9 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=df.iloc[9][0]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[9][1])]),
                ])
    return [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5, table_rows6, table_rows7, table_rows8, table_rows9])]

def get_news_content(value, date, time):
    if value in data_kpi:
        # value for header
        name = value

        # small letter for dict
        if " " in value:
            value = value.replace(" ", "_")
        if "." in value:
            value = value.replace(".", "")

        value = value.lower()

        wkns_and_isins = api_call_value("wkns_and_isins", value)

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

        #Table Unternehmensnews

        table_body = get_table_rows_first(df)

        # widget-one-news

        widget_one_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Unternehmensnews"),
                        html.Div(children=[
                            dbc.Table(table_body)
                        ]),     
                    ]
                )
            ],
        )

        #worker reviews
        worker_reviews = api_call_value_date_time('worker_reviews', value, date, time)

        worker_reviews_positive = []
        worker_reviews_negative = []
        worker_reviews_suggestions = []

        for entry in worker_reviews:
            if 'negative_reviews' in entry:
                worker_reviews_negative.append(entry['negative_reviews'])
            elif 'positive_reviews' in entry:
                worker_reviews_positive.append(entry['positive_reviews'])
            elif 'suggestions' in entry:
                worker_reviews_suggestions.append(entry['suggestions'])

        df_worker_reviews_negative = pd.DataFrame(worker_reviews_negative)
        df_worker_reviews_positive = pd.DataFrame(worker_reviews_positive)
        df_worker_reviews_suggestions = pd.DataFrame(worker_reviews_suggestions)

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
                                    html.P(id= 'news_company_review_text', children=df_worker_reviews_negative['negative'][0]),
                                    html.P(id= 'news_company_review_text', children=df_worker_reviews_negative['negative'][1]),
                                ])
                            ]),
                            html.Div(id ='news_latest_negative',children=[
                                html.P(children='Latest Negative'),
                                html.Div(id = 'news_company_review', children = [
                                    html.P(id= 'news_company_review_text', children=df_worker_reviews_positive['positive'][0]),
                                    html.P(id= 'news_company_review_text', children=df_worker_reviews_positive['positive'][1]),
                                ])
                            ]),
                            html.Div(id ='news_suggestion',children=[
                                html.P(children='Suggestion'),
                                html.Div(id = 'news_company_review', children = [
                                    html.P(id= 'news_company_review_text', children=df_worker_reviews_suggestions['suggestions'][0]),
                                ])
                            ])
                        ]),     
                    ]
                )
            ],
        )

        #Kunden
        customer_experience_date_time = api_call_value_date_time('customer_experience', value, date, time)

        df_customer_experience = pd.DataFrame(customer_experience_date_time)
        customer_experience_dataframe = pd.DataFrame()
        customer_experience_dataframe[' '] = df_customer_experience['title']
        customer_experience_dataframe['Klassifizierung'] = df_customer_experience['class']

        table_body_two = get_table_rows_secound(customer_experience_dataframe)

        # widget-three-news
        widget_three_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Kundenrezesionen"),
                        html.Div(children=[
                            dbc.Table(table_body_two)
                        ]),     
                    ]
                )
            ],
        )

        #Dax News
        dax_news_date_time = api_call_date_time('dax_news' , date, time)
        dax_news = []

        for entry in dax_news_date_time:
            dax_news.append(entry['news'])

        df_dax_news = pd.DataFrame(dax_news)
        dax_news_dataframe = pd.DataFrame()
        dax_news_dataframe[' '] = df_dax_news['headline']
        dax_news_dataframe['Zeitpunkt'] = df_dax_news['timestamp']

        # widget-four-news
        widget_four_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="DAX-News"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(dax_news_dataframe[0:6])
                        ]),     
                    ]
                )
            ],
        )

        #Global News
        date_time = api_call_date_time('world_news_by_date' , date, time)
        date_time = date_time[1:]
        worker_reviews = []

        for entry in date_time:
            worker_reviews.append(entry['headline'])

        df_worker_reviews = pd.DataFrame(worker_reviews)
        worker_reviews_dataframe = pd.DataFrame()
        worker_reviews_dataframe[' '] = df_worker_reviews['headline']
        worker_reviews_dataframe['Zeitpunkt'] = df_worker_reviews['timestamp']

        # widget-five-news
        widget_five_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Globale News"),
                        html.Div(children=[
                            dbc.Table.from_dataframe(worker_reviews_dataframe[0:6])
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
