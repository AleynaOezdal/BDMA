import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime



# # https://stooq.com/
# start = datetime.datetime(2020, 1, 1)
# end = datetime.datetime(2020, 12, 3)
# df = web.DataReader(['Stunde','7 Tage','14 Tage','1 Monat'],
#                     'stooq', start=start, end=end)
# # df=df.melt(ignore_index=False, value_name="price").reset_index()
# df = df.stack().reset_index()

# colors = {
#     'background': '#F6F6F6'
# }

# font = {
#     'helvetica' : 'Arial, Helvetica, sans-serif'
# }

# #style widget
# style_widget_news = {
#     'width': '48%',
#     'display': 'inline-block',
#     'vertical-align': 'middle',
#     'background': colors['background'],
#     'margin': '1%'

# }

def get_content_home():
    content = html.Div(id = 'content',children=[html.P(children= 'Hello')])
    return content 

# def get_content_home_2():
#     content = dbc.Container([

#         dbc.Row([
#             dbc.Col([
#                 html.H1("Good Morning Mr.CEO", style={'textAlign': 'center'})
#             ], width=12)
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 html.H2('Team Dashboard wishes you a sucessful day with right decisions!', style={'textAlign': 'center'})
#             ], width=12)
#         ]),

#         dbc.Row([

#             dbc.Col([
#                 dcc.Dropdown(id='my-dpdn2', multi=True, value=['Stunde', '7 Tage', '14 Tage', '1 Monat'],
#                             options=[{'label': x, 'value': x}
#                                     for x in sorted(df['Symbols'].unique())],
#                             ),
#                 dcc.Graph(id='line-fig2', figure={})
#             ],  # width={'size':5, 'offset':0, 'order':2},
#                 xs=12, sm=12, md=12, lg=5, xl=5
#             ),

#         ], justify='start'),

#         dbc.Row(id = 'widget-one', children =[
#                                 html.Div(children=[
#                                     html.H4(children = 'NEWS', style={'font-size': '100%'}),
#                                     html.P(children='yfinance oder finanzen.net', style={'font-size': '80%'}),
#                                     html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
#                                 ], style={
#                                     'width': '40%',
#                                     'margin': '8%',
#                                     'display': 'inline-block'
#                                 })
#                             ], style=style_widget_news),

#     ], fluid=True)
#     return content


# # Callback section: connecting the components
# # ************************************************************************
# # Line chart - multiple


