from unittest import skip
from dash import dcc, html
import plotly.express as px
import pandas as pd
from zmq import EMSGSIZE
from retrieve_sample_data import get_stocks_data, get_news_data, get_kpi_data
from sidebar import data_kpi
from retrieve_mongo_db import *
from company_dic import *

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
        wkns_and_isins = get_wkns_and_isins(value)

        #content-header-kpi
        content_header_kpi  = html.H3(id = 'content-header', children=['Key Performance Indicators for '+ name+' '+wkns_and_isins])

        #get wiget data free cashflow
        if get_esg_score(company_dict[value]) != 0:
             esg = get_esg_score(company_dict[value])
        else:
            esg = 0
        
        widget_one_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Free Cashflow in MEUR'),
                                html.P(id='kpi_widget_key', children= esg),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})  
                        ])

        #get wiget data ebitda
        if get_ebit(company_dict[value])['Ebit'][0] != 0:
             ebit = get_ebit(company_dict[value])['Ebit'][0]
        else:
            ebit = 0
        
        #widget-two-kpi
        widget_two_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'EBIT in MEUR'),
                                html.P(id='kpi_widget_key', children=ebit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])
        
        #get widget data gross profit
        if get_gross_profit(company_dict[value])['Gross Profit'][0] != 0:
             gross_profit = get_gross_profit(company_dict[value])['Gross Profit'][0]
        else:
            gross_profit = 0

        #widget-three-kpi
        widget_three_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Profit Margin in %'),
                                html.P(id='kpi_widget_key', children=gross_profit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])
        
        #get wiget data level
        if get_net_income(company_dict[value])['Net Income'][0] != 0:
             income = get_net_income(company_dict[value])['Net Income'][0]
        else:
            income = 0

        #widget-four-kpi
        widget_four_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Net income'),
                                html.P(id='kpi_widget_key', children=income),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])

        #get widget data revenue
        if get_total_revenue(company_dict[value])['Total Revenue'][0] != 0:
             revenue = get_total_revenue(company_dict[value])['Total Revenue'][0]
        else:
            revenue = 0

        #widget-five-kpi
        widget_five_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Revenue in MEUR'),
                                html.P(id='kpi_widget_key', children=revenue),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])

        #get wiget data level
        if get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0] != 0:
             level = get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0]
        else:
            level = 0
        
        #widget-six-kpi
        widget_six_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Total operating expenses'),
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