from dash import dcc, html
from numpy import negative
import pandas as pd
from sidebar import data_kpi
from setup import create_company_dict
import dash_bootstrap_components as dbc
from company_map import *
import requests as req
import arrow

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
    table_header = [html.Thead(html.Tr([html.Th(" "), html.Th("Datum"), html.Th(html.Th(id='tumbs_header',children=[
                        html.I(className='bi bi-hand-thumbs-up-fill'),
                        html.P(id='tumbs_header_text',children='/'),
                        html.I(className='bi bi-hand-thumbs-down-fill')    
                    ]))]))]

    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[0][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[0][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[0][1][8:10]+'.'+df.iloc[0][1][5:7]+'.'+df.iloc[0][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[0][2])]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[1][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[1][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[1][1][8:10]+'.'+df.iloc[1][1][5:7]+'.'+df.iloc[1][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[1][2])]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[2][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[2][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[2][1][8:10]+'.'+df.iloc[2][1][5:7]+'.'+df.iloc[2][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[2][2])]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[3][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[3][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[3][1][8:10]+'.'+df.iloc[3][1][5:7]+'.'+df.iloc[3][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[3][2])]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[4][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[4][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[4][1][8:10]+'.'+df.iloc[4][1][5:7]+'.'+df.iloc[4][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[4][2])]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[5][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[5][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[5][1][8:10]+'.'+df.iloc[5][1][5:7]+'.'+df.iloc[5][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[5][2])]),
                ])
    
    table_body = [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5])]

    return table_header+table_body

def get_table_rows_secound(df):
    table_header = [html.Thead(html.Tr([html.Th(" "), html.Th(id='tumbs_header',children=[
                        html.I(className='bi bi-hand-thumbs-up-fill'),
                        html.P(id='tumbs_header_text',children='/'),
                        html.I(className='bi bi-hand-thumbs-down-fill')    
                    ])]))]

    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[0][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[0][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[0][1])]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[1][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[1][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[1][1])]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[2][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[2][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[2][1])]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[3][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[3][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[3][1])]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[4][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[4][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[4][1])]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[5][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[5][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[5][1])]),
                ])

    table_rows6 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[6][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[6][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[6][1])]),
                ])

    table_rows7 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[7][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[7][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[7][1])]),
                ])
    
    table_rows8 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[8][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[8][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[8][1])]),
                ])

    table_rows9 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text',children=df.iloc[9][0]),
                        html.A(id='table_td_link_rezension',children='Ganze Rezension lesen',href=df.iloc[9][2],target="_blank")]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[9][1])]),
                ])
     
    table_body = [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5, table_rows6, table_rows7, table_rows8, table_rows9])]

    return table_header+table_body

def get_table_rows_three(df):

    table_header = [html.Thead(html.Tr([html.Th(" "), html.Th('Datum')]))]

    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[5][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[5][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[5][1]]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[4][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[4][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=df.iloc[4][1]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[3][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[3][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=df.iloc[3][1]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[2][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[2][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=df.iloc[2][1]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[1][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[1][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=df.iloc[1][1]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[0][0]),
                        html.A(id='table_td_link_rezension',children='Ganzen Artikel lesen',href=df.iloc[0][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=df.iloc[0][1]),
                ])
    
    table_body = [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5])]

    return table_header+table_body

def get_table_rows_four(df):

    table_header = [html.Thead(html.Tr([html.Th(" "), html.Th('Datum')]))]

    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.A(id='table_td_link',children=df.iloc[5][0],href=df.iloc[5][2],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[5][1]]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.A(id='table_td_link',children=df.iloc[4][0],href=df.iloc[4][2],target="_blank")]),
                    html.Td(id='table_td', children=df.iloc[4][1]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.A(id='table_td_link',children=df.iloc[3][0],href=df.iloc[3][2],target="_blank")]),
                    html.Td(id='table_td', children=df.iloc[3][1]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.A(id='table_td_link',children=df.iloc[2][0],href=df.iloc[2][2],target="_blank")]),
                    html.Td(id='table_td', children=df.iloc[2][1]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.A(id='table_td_link',children=df.iloc[1][0],href=df.iloc[1][2],target="_blank")]),
                    html.Td(id='table_td', children=df.iloc[1][1]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.A(id='table_td_link',children=df.iloc[0][0],href=df.iloc[0][2],target="_blank")]),
                    html.Td(id='table_td', children=df.iloc[0][1]),
                ])
    
    table_body = [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5])]

    return table_header+table_body

def get_table_rows_last(df):
    table_header = [html.Thead(html.Tr([html.Th(" "), html.Th("Datum"), html.Th(html.Th(id='tumbs_header',children=[
                        html.I(className='bi bi-hand-thumbs-up-fill'),
                        html.P(id='tumbs_header_text',children='/'),
                        html.I(className='bi bi-hand-thumbs-down-fill')    
                    ]))]))]

    table_rows0 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[0][0][:50]+'...'),
                        html.A(id='table_td_link_rezension',children='Ganzen Beitrag lesen',href=df.iloc[0][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[0][1][8:10]+'.'+df.iloc[0][1][5:7]+'.'+df.iloc[0][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[0][2])]),
                ])

    table_rows1 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[1][0][:50]+'...'),
                        html.A(id='table_td_link_rezension',children='Ganzen Beitrag lesen',href=df.iloc[1][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[1][1][8:10]+'.'+df.iloc[1][1][5:7]+'.'+df.iloc[1][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[1][2])]),
                ])
    
    table_rows2 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[2][0][:50]+'...'),
                        html.A(id='table_td_link_rezension',children='Ganzen Beitrag lesen',href=df.iloc[2][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[2][1][8:10]+'.'+df.iloc[2][1][5:7]+'.'+df.iloc[2][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[2][2])]),
                ])

    table_rows3 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[3][0][:50]+'...'),
                        html.A(id='table_td_link_rezension',children='Ganzen Beitrag lesen',href=df.iloc[3][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[3][1][8:10]+'.'+df.iloc[3][1][5:7]+'.'+df.iloc[3][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[3][2])]),
                ])

    table_rows4 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[4][0][:50]+'...'),
                        html.A(id='table_td_link_rezension',children='Ganzen Beitrag lesen',href=df.iloc[4][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[4][1][8:10]+'.'+df.iloc[4][1][5:7]+'.'+df.iloc[4][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[4][2])]),
                ])

    table_rows5 = html.Tr(id='table_tr', children=[
                    html.Td(id='table_td', children=[
                        html.P(id='table_td_text', children=df.iloc[5][0][:50]+'...'),
                        html.A(id='table_td_link_rezension',children='Ganzen Beitrag lesen',href=df.iloc[5][3],target="_blank")
                    ]),
                    html.Td(id='table_td', children=[df.iloc[5][1][8:10]+'.'+df.iloc[5][1][5:7]+'.'+df.iloc[5][1][:4]]),
                    html.Td(id='table_td', children=[get_thumbs(df.iloc[5][2])]),
                ])

    table_body = [html.Tbody([table_rows0, table_rows1, table_rows2, table_rows3, table_rows4, table_rows5])]

    return table_header+table_body

# valuecount = df['Klasse'].value_counts()
# negativ = valuecount["Negativ"]
# positiv = valuecount["Positiv"]

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

        #Unternehmensnews
        company_news_date_time = api_call_value_date_time('company_news_classified' , value, date, time)

        df_company_news = pd.DataFrame(company_news_date_time)

        company_news_dataframe = pd.DataFrame()
        company_news_dataframe[' '] = df_company_news['headline']
        company_news_dataframe['Time'] = df_company_news['timestamp']
        company_news_dataframe['Klassifizierung'] = df_company_news['class']
        company_news_dataframe['more_info'] = df_company_news['more_info']

        df_company_news_24 = pd.DataFrame(api_call_value_date_time('company_news_classified_24h' , value, date, time))

        valuecount = df_company_news_24['class'].value_counts()
        negative = (valuecount['NEGATIVE']/(valuecount['NEGATIVE']+valuecount['POSITIVE'])*100)
        positive = (valuecount['POSITIVE']/(valuecount['NEGATIVE']+valuecount['POSITIVE'])*100)

        table_body = get_table_rows_first(company_news_dataframe)

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
                        html.P(id='table_td_text_tumbs', children=[
                            'Anteil ',
                            html.I(className='bi bi-hand-thumbs-up-fill'),
                            ' News letzte 24h: ',
                            round(positive, 2),
                            '%'
                        ]),
                        html.P(id='table_td_text_tumbs', children=[
                            'Anteil ',
                            html.I(className='bi bi-hand-thumbs-down-fill'),
                            ' News letzte 24h: ',
                            round(negative, 2),
                            '%'
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
                                    html.Div(id= 'news_company_review_div', children=[
                                        html.P(id='news_company_review_text',children=[df_worker_reviews_negative['negative'][0][:80]+'...']),
                                        html.A(id='show_more', children='Mehr anzeigen', href=df_worker_reviews_negative['more info'][0],target="_blank")
                                    ]),
                                    html.Div(id= 'news_company_review_div', children=[
                                        html.P(id='news_company_review_text',children=[df_worker_reviews_negative['negative'][1][:80]+'...']),
                                        html.A(id='show_more', children='Mehr anzeigen', href=df_worker_reviews_negative['more info'][1],target="_blank")
                                    ])
                                ])
                            ]),
                            html.Div(id ='news_latest_negative',children=[
                                html.P(children='Latest Negative'),
                                html.Div(id = 'news_company_review', children = [
                                    html.Div(id= 'news_company_review_div', children=[
                                        html.P(id='news_company_review_text',children=[df_worker_reviews_positive['positive'][0][:80]+'...']),
                                        html.A(id='show_more', children='Mehr anzeigen', href=df_worker_reviews_positive['more info'][0],target="_blank")
                                    ]),
                                    html.Div(id= 'news_company_review_div', children=[
                                        html.P(id='news_company_review_text',children=[df_worker_reviews_positive['positive'][1][:80]+'...']),
                                        html.A(id='show_more', children='Mehr anzeigen', href=df_worker_reviews_positive['more info'][1],target="_blank")
                                    ])
                                ])
                            ]),
                            html.Div(id ='news_suggestion',children=[
                                html.P(children='Suggestion'),
                                html.Div(id = 'news_company_review', children = [
                                    html.Div(id= 'news_company_review_div', children=[
                                        html.P(id='news_company_review_text',children=[df_worker_reviews_suggestions['suggestions'][0][:80]+'...']),
                                        html.A(id='show_more', children='Mehr anzeigen', href=df_worker_reviews_suggestions['more info'][0],target="_blank")
                                    ])
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
        customer_experience_dataframe['more info'] = df_customer_experience['more_info']

        df_customer_experience_24 = pd.DataFrame(api_call_value_date_time('customer_experience_24h' , value, date, time))

        valuecount = df_customer_experience_24['class'].value_counts()
        negative = (valuecount['NEGATIVE']/(valuecount['NEGATIVE']+valuecount['POSITIVE'])*100)
        positive = (valuecount['POSITIVE']/(valuecount['NEGATIVE']+valuecount['POSITIVE'])*100)

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
                        html.P(id='table_td_text_tumbs', children=[
                            'Anteil ',
                            html.I(className='bi bi-hand-thumbs-up-fill'),
                            ' News letzte 24h: ',
                            round(positive, 2),
                            '%'
                        ]),
                        html.P(id='table_td_text_tumbs', children=[
                            'Anteil ',
                            html.I(className='bi bi-hand-thumbs-down-fill'),
                            ' News letzte 24h: ',
                            round(negative, 2),
                            '%'
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
        dax_news_dataframe['Datum'] = df_dax_news['timestamp']
        dax_news_dataframe['more_info'] = df_dax_news['more_info']

        for index, row in dax_news_dataframe.iterrows():
            if 'Uhr' in row['Datum']:
                row['Datum'] = arrow.now().format('DD.MM.YY')

        table_body_three = get_table_rows_three(dax_news_dataframe)

        # widget-four-news
        widget_four_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="DAX-News"),
                        html.Div(children=[
                            dbc.Table(table_body_three)
                        ]),     
                    ]
                )
            ],
        )

        #Global News
        world_news_date_time = api_call_date_time('world_news_by_date' , date, time)
        world_news = []

        for entry in world_news_date_time:
            if 'headline' in entry:
                world_news.append(entry['headline'])

        for entry in world_news:
            if entry == 'NaN':
                world_news.remove(entry)

        df_world_news = pd.DataFrame(world_news)
        world_news_dataframe = pd.DataFrame()
        world_news_dataframe[' '] = df_world_news['headline']
        world_news_dataframe['Datum'] = df_world_news['timestamp']
        world_news_dataframe['more_info'] = df_world_news['more_info']

        for index, row in world_news_dataframe.iterrows():
            if 'Uhr' in row['Datum']:
                row['Datum'] = arrow.now().format('DD.MM.YY')

        table_body_four = get_table_rows_three(world_news_dataframe)

        # widget-five-news
        widget_five_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Globale News"),
                        html.Div(children=[
                            dbc.Table(table_body_four)
                        ]),     
                    ]
                )
            ],
        )

        #Community News
        community_news_date_time = api_call_value_date_time('community_news' , value, date, time)

        df_community_news = pd.DataFrame(community_news_date_time)

        community_news_dataframe = pd.DataFrame()
        community_news_dataframe[' '] = df_community_news['message']
        community_news_dataframe['Time'] = df_community_news['timestamp']
        community_news_dataframe['Klassifizierung'] = df_community_news['class']
        community_news_dataframe['more_info'] = df_community_news['more_info']

        df_community_news_24 = pd.DataFrame(api_call_value_date_time('community_news_24h' , value, date, time))

        valuecount = df_community_news_24['class'].value_counts()
        negative = (valuecount['NEGATIVE']/(valuecount['NEGATIVE']+valuecount['POSITIVE'])*100)
        positive = (valuecount['POSITIVE']/(valuecount['NEGATIVE']+valuecount['POSITIVE'])*100)

        table_body = get_table_rows_last(community_news_dataframe)

        # widget-six-news
        widget_six_news = html.Div(
            id="news_widget",
            children=[
                html.Div(
                    id="news_widget_content",
                    children=[
                        html.H6(id="news_widget_header", children="Börsen-Community"),
                        html.Div(children=[
                            dbc.Table(table_body)
                        ]),
                        html.P(id='table_td_text_tumbs', children=[
                            'Anteil ',
                            html.I(className='bi bi-hand-thumbs-up-fill'),
                            ' News letzte 24h: ',
                            round(positive, 2),
                            '%'
                        ]),
                        html.P(id='table_td_text_tumbs', children=[
                            'Anteil ',
                            html.I(className='bi bi-hand-thumbs-down-fill'),
                            ' News letzte 24h: ',
                            round(negative, 2),
                            '%'
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
