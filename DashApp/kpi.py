from unittest import skip
from dash import dcc, html
import plotly.express as px
import pandas as pd
from zmq import EMSGSIZE
from retrieve_sample_data import get_stocks_data, get_news_data, get_kpi_data
from sidebar import data_kpi

#figure for widget
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    'x': [1,2,1,2],
    'y': [1,2,3,4],
    'customdata': [1,2,3,4],
    'fruit': ['apple', 'apple', 'orange', 'orange']
})

fig = px.scatter(df, x='x', y='y', color='fruit', custom_data=['customdata'])

#widget one graph
fig.update_layout(
    height = 80,
    showlegend=False,
    margin_l = 0,
    margin_r = 0,
    margin_t = 0,
    margin_b = 0,
)

def get_value_without_kpi(value):
    if value == 'None':
        content  = html.H3(id = 'content-header', children=['Select a Company'])
        return content
    else:
        content  = html.H3(id = 'content-header', children=['Select a navigation point'])
        return content

def get_kpi_content_value(value):
    if value in data_kpi:
        #big letter 
        name = value.title()

        #content-header-kpi
        content_header_kpi  = html.H3(id = 'content-header', children=['Key Performance Indicators for '+ name])

        #get wiget data free cashflow
        free_cf = 0

        for entry in get_kpi_data():
            if value == entry['_id']:
                if 'free_cf' in entry:
                    free_cf = entry['free_cf']
                else:
                    pass
            else:
                pass
        
        widget_one_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Free Cashflow in MEUR'),
                                html.P(id='kpi_widget_key', children= free_cf),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})  
                        ])

        #get wiget data ebitda
        ebitda = 0

        for entry in get_kpi_data():
            if value == entry['_id']:
                if 'ebitda' in entry:
                    ebitda = entry['ebitda']
                else:
                    pass
            else:
                pass
        
        #widget-two-kpi
        widget_two_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'EBITDA in MEUR'),
                                html.P(id='kpi_widget_key', children=ebitda),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])
        
        #get widget data gross profit
        gross_profit = 0

        for entry in get_kpi_data():
            if value == entry['_id']:
                if 'gross_profit' in entry:
                    gross_profit = entry['gross_profit']
                else:
                    pass
            else:
                pass

        #widget-three-kpi
        widget_three_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Profit Margin in %'),
                                html.P(id='kpi_widget_key', children=gross_profit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])
        
        #get wiget data level
        esg = 0

        for entry in get_kpi_data():
            if value == entry['_id']:
                if 'esg' in entry:
                    esg = entry['esg']
                else:
                    pass
            else:
                pass

        #widget-four-kpi
        widget_four_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'ESG Risk Score'),
                                html.P(id='kpi_widget_key', children=esg),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])

        #get widget data revenue
        revenue = 0

        for entry in get_kpi_data():
            if value == entry['_id']:
                if 'revenue' in entry:
                    revenue = entry['revenue']
                else:
                    pass
            else:
                pass

        #widget-five-kpi
        widget_five_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Revenue in MEUR'),
                                html.P(id='kpi_widget_key', children=revenue),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])

        #get wiget data level
        level = 0

        for entry in get_kpi_data():
            if value == entry['_id']:
                if 'level' in entry:
                    level = entry['level']
                else:
                    pass
            else:
                pass
        
        #widget-six-kpi
        widget_six_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Controversy Level'),
                                html.P(id='kpi_widget_key', children=level),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]) 
                        ])

        content = html.Div(id = 'content', children=[
                        content_header_kpi,
                        html.Div(id = 'widget', children = [ 
                            widget_one_kpi,
                            widget_two_kpi,
                            widget_three_kpi,
                            widget_four_kpi,
                            widget_five_kpi,
                            widget_six_kpi,
                        ])
                    ])
        
        return content
    else:
        content_header_kpi  = html.H3(id = 'content-header', children=['Select a Company'])
        return content_header_kpi