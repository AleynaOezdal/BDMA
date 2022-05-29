from unittest import skip
from dash import dcc, html
import plotly.express as px
import pandas as pd
from zmq import EMSGSIZE
from sidebar import data_kpi
from retrieve_mongo_db import *
from company_dic import *

#get short numbers 
def short_num(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', ' Tausend', ' MIO.', ' MRD.', ' BIO.', ' Trillionen'][magnitude])

def get_value_without_kpi(value):
    if value == 'None':
        content  = html.H3(id = 'content-header', children=['Wählen Sie ein Unternehmen aus'])
        return content
    else:
        content  = html.H3(id = 'content-header', children=['Wählen Sie ein Navigationspunkt aus'])
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
            if esg >= 40:
                high_average_low = 'SERVER'
                color = 'red'
            elif esg <= 40 and esg >= 30:
                high_average_low = 'HIGH'
                color = 'orange'
            elif esg <= 30 and esg >= 20:
                high_average_low = 'MEDIUM'
                color = 'orange'    
            elif esg <= 20 and esg >= 10:
                high_average_low = 'LOW'
                color = 'green'
            elif esg <= 10:
                high_average_low = 'NEGLIGIBLE'
                color= 'green'
        else:
            esg = 0
            high_average_low = 'LOW'
            color= 'green'

        
        widget_esg_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'ESG Risk Score'),
                                html.P(id='kpi_widget_key', children= esg),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph_text', children= [
                                html.P(id='kpi_widget_esg', children=high_average_low, style={'color': color})
                            ])
                        ])

        #get wiget data ebit
        if get_ebit(company_dict[value])['Ebit'][0] != 0:
             ebit = short_num(get_ebit(company_dict[value])['Ebit'][0])
        else:
            ebit = 0
        
        fig_ebit = px.bar(get_ebit(company_dict[value]), y='Ebit', text_auto = True, labels={'Ebit': '',  'index': ''})
        
        fig_ebit.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            paper_bgcolor = '#F6F6F6'
        )

        widget_ebit_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'EBIT'),
                                html.P(id='kpi_widget_key', children=ebit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_ebit
                            )])])
        
        #get widget data gross profit
        if get_gross_profit(company_dict[value])['Gross Profit'][0] != 0:
             gross_profit = short_num(get_gross_profit(company_dict[value])['Gross Profit'][0])
        else:
            gross_profit = 0

        fig_gross_profit = px.bar(get_gross_profit(company_dict[value]), x='Gross Profit', text_auto = True, orientation='h',labels={'Gross Profit': '',  'index': ''})

        fig_gross_profit.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
            paper_bgcolor = '#F6F6F6'
        )

        widget_gross_profit_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Profit Margin'),
                                html.P(id='kpi_widget_key', children=gross_profit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_gross_profit
                            )])
                        ])
        
        #get wiget data net income
        if get_net_income(company_dict[value])['Net Income'][0] != 0:
             income = short_num(get_net_income(company_dict[value])['Net Income'][0])
        else:
            income = 0

        df = get_net_income(company_dict[value]).sort_index()
        fig_net_income = px.line(df, y='Net Income', labels={'Net Income': '',  'index': ''})

        fig_net_income.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
            paper_bgcolor = '#F6F6F6'
        )

        widget_net_income_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Net income'),
                                html.P(id='kpi_widget_key', children=income),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_net_income
                            )])
                        ])

        #get widget data total revenue
        if get_total_revenue(company_dict[value])['Total Revenue'][0] != 0:
             revenue = short_num(get_total_revenue(company_dict[value])['Total Revenue'][0])
        else:
            revenue = 0
        
        fig_total_revenue = px.bar(get_total_revenue(company_dict[value]), x='Total Revenue', text_auto = True, orientation='h', labels={'Total Revenue': '',  'index': ''})

        fig_total_revenue.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
            paper_bgcolor = '#F6F6F6'
        )

        widget_total_revenue_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Revenue'),
                                html.P(id='kpi_widget_key', children=revenue),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_total_revenue
                            )])
                        ])

        #get wiget data total operating expenses
        if get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0] != 0:
             level = short_num(get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0])
        else:
            level = 0
        
        fig_total_operating_expenses = px.bar(get_total_operating_expenses(company_dict[value]), x='Total Operating Expenses', orientation='h', text_auto = True, labels={'Total Operating Expenses': '',  'index': ''})

        fig_total_operating_expenses.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
            paper_bgcolor = '#F6F6F6'
        )

        #widget-six-kpi
        widget_total_operating_expenses_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Total operating expenses'),
                                html.P(id='kpi_widget_key', children=level),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_total_operating_expenses
                            )])
                        ])

        content = html.Div(id = 'content', children=[
                        content_header_kpi,
                        html.Div(id = 'widget', children = [ 
                            widget_ebit_kpi,
                            widget_total_revenue_kpi,
                            widget_gross_profit_kpi,
                            widget_net_income_kpi,
                            widget_esg_kpi,
                            widget_total_operating_expenses_kpi
                        ])
                    ])
        
        return content
    else:
        content_header_kpi  = html.H3(id = 'content-header', children=['Select a Company'])
        return content_header_kpi