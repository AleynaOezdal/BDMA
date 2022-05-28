from unittest import skip
from dash import dcc, html
import plotly.express as px
import pandas as pd
from zmq import EMSGSIZE
from sidebar import data_kpi
from retrieve_mongo_db import *
from company_dic import *


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
        else:
            esg = 0
        
        widget_esg_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'ESG Scroe'),
                                html.P(id='kpi_widget_key', children= esg),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ])])

        #get wiget data ebit
        if get_ebit(company_dict[value])['Ebit'][0] != 0:
             ebit = get_ebit(company_dict[value])['Ebit'][0]
        else:
            ebit = 0
        
        fig_ebit = px.bar(get_ebit(company_dict[value]), y='Ebit',text_auto = True)
        
        fig_ebit.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
        )

        widget_ebit_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'EBIT in MEUR'),
                                html.P(id='kpi_widget_key', children=ebit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig_ebit
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})
                        ])
        
        #get widget data gross profit
        if get_gross_profit(company_dict[value])['Gross Profit'][0] != 0:
             gross_profit = get_gross_profit(company_dict[value])['Gross Profit'][0]
        else:
            gross_profit = 0

        fig_gross_profit = px.bar(get_gross_profit(company_dict[value]), y='Gross Profit',text_auto = True)

        fig_gross_profit.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
        )

        widget_gross_profit_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Profit Margin in %'),
                                html.P(id='kpi_widget_key', children=gross_profit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig_gross_profit
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})
                        ])
        
        #get wiget data net income
        if get_net_income(company_dict[value])['Net Income'][0] != 0:
             income = get_net_income(company_dict[value])['Net Income'][0]
        else:
            income = 0
        
        fig_net_income = px.bar(get_net_income(company_dict[value]), y='Net Income',text_auto = True)

        fig_net_income.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
        )

        widget_net_income_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Net income'),
                                html.P(id='kpi_widget_key', children=income),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig_net_income
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})
                        ])

        #get widget data total revenue
        if get_total_revenue(company_dict[value])['Total Revenue'][0] != 0:
             revenue = get_total_revenue(company_dict[value])['Total Revenue'][0]
        else:
            revenue = 0
        
        fig_total_revenue = px.bar(get_total_revenue(company_dict[value]), y='Total Revenue',text_auto = True)

        fig_total_revenue.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
        )

        widget_total_revenue_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Revenue in MEUR'),
                                html.P(id='kpi_widget_key', children=revenue),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig_total_revenue
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})
                        ])

        #get wiget data total operating expenses
        if get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0] != 0:
             level = get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0]
        else:
            level = 0
        
        fig_total_operating_expenses = px.bar(get_total_operating_expenses(company_dict[value]), y='Total Operating Expenses',text_auto = True)

        fig_total_operating_expenses.update_layout(
            height = 90,
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            title_y = False,
            title_x = False,
        )

        #widget-six-kpi
        widget_total_operating_expenses_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Total operating expenses'),
                                html.P(id='kpi_widget_key', children=level),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig_total_operating_expenses
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})
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