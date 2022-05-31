from unittest import skip
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from sidebar import data_kpi
from retrieve_mongo_db import *
from producersetup import create_company_dict
import dash_bootstrap_components as dbc
from dict import *

company_dict = create_company_dict()

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
        #value for header
        name = value

        #small letter for dict
        if ' ' in value:
            value = value.replace(' ', '_')
        if '.' in value:
            value = value.replace('.','')

        value = value.lower()

        wkns_and_isins = get_wkns_and_isins(value)

        #content-header-kpi
        content_header_kpi  = html.Div(id ='content_header_kpi', children=[
                                html.H3(id = 'content_header_first', children=['Key Performance Indicators ']),
                                html.H3(id = 'content_header_second', children=['for']),
                                html.H3(id = 'content_header_third', children=[name+' '+wkns_and_isins])
                            ])
            

        #get wiget data ebit
        if get_ebit(company_dict[value])['Ebit'][0] != 0 and get_ebit(company_dict[value])['Ebit'][0] != 'NaN':
             ebit = short_num(get_ebit(company_dict[value])['Ebit'][0])
        else:
            ebit = 0
      
        ebit_df = get_ebit(company_dict[value]).sort_index()

        fig_ebit = go.Figure(go.Scatter(y=ebit_df['Ebit'], x=ebit_df.index))
        
        fig_ebit.update_traces(mode='lines', line_color='#EA000D')

        fig_ebit.update_layout(
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            paper_bgcolor = '#F6F6F6',
            plot_bgcolor = '#F6F6F6',
            uniformtext_minsize=6,
        )

        widget_ebit_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'EBIT'),
                                html.P(id='kpi_widget_key', children=ebit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_ebit,
                                style={'width': '20vmax', 'height': '10vmax'}
                            )])
                        ])
        
        #get widget data gross profit
        if get_gross_profit(company_dict[value])['Gross Profit'][0] != 0 and get_gross_profit(company_dict[value])['Gross Profit'][0] != 'NaN':
             gross_profit = short_num(get_gross_profit(company_dict[value])['Gross Profit'][0])
        else:
            gross_profit = 0

        gross_profit_df = get_gross_profit(company_dict[value])
        
        fig_gross_profit = go.Figure(go.Bar(x=gross_profit_df['Gross Profit'], y=gross_profit_df.index, text=gross_profit_df['Gross Profit'], orientation='h'))
        fig_gross_profit.update_traces(marker_color='#19AD50', textposition = 'inside', texttemplate='%{text:.3s}')#, marker_line_color='#67E98B', marker_line_width=1.5, opacity=0.6)
        
        fig_gross_profit.update_layout(
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            paper_bgcolor = '#F6F6F6',
            plot_bgcolor = '#F6F6F6',
            uniformtext_minsize=6,
        )

        widget_gross_profit_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Profit Margin'),
                                html.P(id='kpi_widget_key', children=gross_profit),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_gross_profit,
                                style={'width': '20vmax', 'height': '10vmax'}
                            )])
                        ])
        
        #get wiget data net income
        if get_net_income(company_dict[value])['Net Income'][0] != 0 and get_net_income(company_dict[value])['Net Income'][0] != 'NaN':
             income = short_num(get_net_income(company_dict[value])['Net Income'][0])
        else:
            income = 0

        net_income_df = get_net_income(company_dict[value]).sort_index()

        fig_net_income = go.Figure(go.Scatter(y=net_income_df['Net Income'], x=net_income_df.index))

        fig_net_income.update_traces(mode='lines', line_color='#EDA611')

        fig_net_income.update_layout(
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            paper_bgcolor = '#F6F6F6',
            plot_bgcolor = '#F6F6F6',
        )

        widget_net_income_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Net income'),
                                html.P(id='kpi_widget_key', children=income),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_net_income,
                                style={'width': '20vmax', 'height': '10vmax'}
                            )])
                        ])

        #get widget data total revenue
        if get_total_revenue(company_dict[value])['Total Revenue'][0] != 0 and get_total_revenue(company_dict[value])['Total Revenue'][0] != 'NaN':
             revenue = short_num(get_total_revenue(company_dict[value])['Total Revenue'][0])
        else:
            revenue = 0

        total_revenue_df = get_total_revenue(company_dict[value])
        
        fig_total_revenue = go.Figure(go.Bar(y=total_revenue_df['Total Revenue'], x=total_revenue_df.index, text=total_revenue_df['Total Revenue']))
        fig_total_revenue.update_traces(marker_color='#79EB71', textposition = 'inside', texttemplate='%{text:.3s}')#, marker_line_color='#67E98B', marker_line_width=1.5, opacity=0.6)
        
        fig_total_revenue.update_layout(
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            paper_bgcolor = '#F6F6F6',
            plot_bgcolor = '#F6F6F6',
            uniformtext_minsize=6,
        )

        widget_total_revenue_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'Revenue'),
                                html.P(id='kpi_widget_key', children=revenue),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph', children= [
                                dcc.Graph(
                                figure = fig_total_revenue,
                                style={'width': '20vmax', 'height': '10vmax'}
                            )])
                        ])

        #get wiget data total operating expenses
        if get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0] != 0 and get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0] != 'NaN':
             level = short_num(get_total_operating_expenses(company_dict[value])['Total Operating Expenses'][0])
        else:
            level = 0

        total_operating_expenses_df = get_total_operating_expenses(company_dict[value])
        
        fig_total_operating_expenses = go.Figure(go.Bar(x=total_operating_expenses_df['Total Operating Expenses'], y=total_operating_expenses_df.index, text=total_operating_expenses_df['Total Operating Expenses'], orientation='h'))
        fig_total_operating_expenses.update_traces(marker_color='#3368AD', textposition = 'inside', texttemplate='%{text:.3s}')#, marker_line_color='#67E98B', marker_line_width=1.5, opacity=0.6)
        
        fig_total_operating_expenses.update_layout(
            showlegend=False,
            margin_l = 0,
            margin_r = 0,
            margin_t = 0,
            margin_b = 0,
            paper_bgcolor = '#F6F6F6',
            plot_bgcolor = '#F6F6F6',
            uniformtext_minsize=6
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
                                figure = fig_total_operating_expenses,
                                style={'width': '20vmax', 'height': '10vmax'}
                            )])
                        ])
        
        #get wiget data esg risk score
        if get_esg_score(company_dict[value]) != 0 and get_esg_score(company_dict[value]) != 'NaN':
            esg = get_esg_score(company_dict[value])
            if esg >= 40:
                high_average_low = 'SERVER'
                color = 'red'
            elif esg <= 40 and esg >= 30:
                high_average_low = 'HIGH'
                color = 'red'
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
            high_average_low = 'NONE'
            color= 'green'
        
        widget_esg_kpi = html.Div(id = 'kpi_widget', children =[
                            html.Div(id = 'kpi_widget_text', children=[
                                html.P(id='kpi_widget_header', children = 'ESG Risk Score'),
                                html.P(id='kpi_widget_key', children= esg),
                                html.P(id='kpi_widget_pos', children=['▲'])
                            ]),
                            html.Div(id = 'kpi_graph_text', children= [
                                html.P(id='kpi_widget_esg', children=high_average_low, style={'color': color, 'font-size':'2.5vmax'})
                            ])
                        ])
        #description
        description = get_description(value)
        distribution_value = dict_company_names_long[value]
        distribution = get_distribution(distribution_value)

        accordion = html.Div(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            dbc.Row([
                                dbc.Col(html.Div(id='description', children=[html.H6("Beschreibung: "), description]),width= 6,),
                                dbc.Col(html.Div(id="branche", children=[html.H6("Branche: "+distribution)])),
                                dbc.Col(html.Div("Hauptkonkurrent: Adidas, Daimler, Hellofresh"))]),

                            title= "Detaillierte Informationen zum Unternehmen",
                        ),
                    ],
                    flush=True,
                    start_collapsed=True
                ),
        )


        content = html.Div(id = 'content', children=[
                        content_header_kpi,
                        accordion,
                        html.Div(id = 'widget', children = [
                            widget_ebit_kpi,
                            widget_total_revenue_kpi,
                            widget_gross_profit_kpi,
                            widget_net_income_kpi,
                            widget_esg_kpi,
                            widget_total_operating_expenses_kpi,
                        ])
                    ])
        
        return content
    else:
        content_header_kpi  = html.H3(id = 'content-header', children=['Select a Company'])
        return content_header_kpi