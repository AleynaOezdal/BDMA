from unittest import skip
from dash import dcc, html
import plotly.express as px
import pandas as pd
from zmq import EMSGSIZE
from retrieve_sample_data import get_stocks_data, get_news_data, get_kpi_data
from sidebar import data_kpi

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

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
    font_family=font['helvetica'],
    height = 80,
    showlegend=False,
    margin_l = 0,
    margin_r = 0,
    margin_t = 0,
    margin_b = 0,
    paper_bgcolor = colors['background']
)

#style widget 
style_widget_kpi = {
    'width': '48%' , 
    'display': 'inline-block', 
    'vertical-align': 'middle', 
    'background': colors['background'], 
    'margin': '1%'

}


def get_value_without_kpi(value):
    if value == 'None':
        content  = html.H3(id = 'content-header', children=['Select a Company'], style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            })
        return content
    else:
        content  = html.H3(id = 'content-header', children=['Select a navigation point'], style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            })
        return content

def get_kpi_content_value(value):
    if value in data_kpi:
        #big letter 
        name = value.title()

        #content-header-kpi
        content_header_kpi  = html.H3(id = 'content-header', children=['Key Performance Indicators for '+ name], style={
                    'font-family': font['helvetica'],
                    'font-weight': 'bold', 
                    'margin': '1%'
                })

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
        
        widget_one_kpi = html.Div(id = 'widget-one', children =[
                            html.Div(children=[
                                html.P(children = 'Free Cashflow in MEUR', style={'font-size': '80%'}),
                                html.P(children= free_cf, style={'font-size': '200%', 'font-weight': 'bold'}),
                                html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                            ], style={
                                'width': '40%', 
                                'margin': '5%',
                                'display': 'inline-block'
                            }),
                            html.Div(id = 'graph-one', children= [
                                dcc.Graph(
                                figure = fig
                            )],style = {'width': '40%' , 'display': 'inline-block', 'margin': '5%'})  
                        ], style = style_widget_kpi)

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
        widget_two_kpi = html.Div(id = 'widget-two', children =[
                            html.Div(children=[
                                html.P(children = 'EBITDA in MEUR', style={'font-size': '80%'}),
                                html.P(children=ebitda, style={'font-size': '200%', 'font-weight': 'bold'}),
                                html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                            ], style={
                                'width': '50%', 
                                'margin': '5%'
                            })   
                        ], style = style_widget_kpi)
        
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
        widget_three_kpi = html.Div(id = 'widget-three', children =[
                            html.Div(children=[
                                html.P(children = 'Profit Margin in %', style={'font-size': '80%'}),
                                html.P(children=gross_profit, style={'font-size': '200%', 'font-weight': 'bold'}),
                                html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                            ], style={
                                'width': '50%', 
                                'margin': '5%'
                            }) 
                        ], style = style_widget_kpi)
        
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
        widget_four_kpi = html.Div(id = 'widget-four', children =[
                            html.Div(children=[
                                html.P(children = 'ESG Risk Score', style={'font-size': '80%'}),
                                html.P(children=esg, style={'font-size': '200%', 'font-weight': 'bold'}),
                                html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                            ], style={
                                'width': '50%', 
                                'margin': '5%'
                            })  
                        ], style = style_widget_kpi)

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
        widget_five_kpi = html.Div(id = 'widget-five', children =[
                            html.Div(children=[
                                html.P(children = 'Revenue in MEUR', style={'font-size': '80%'}),
                                html.P(children=revenue, style={'font-size': '200%', 'font-weight': 'bold'}),
                                html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                            ], style={
                                'width': '50%', 
                                'margin': '5%'
                            })   
                        ], style = style_widget_kpi)

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
        widget_six_kpi = html.Div(id = 'widget-six', children =[
                            html.Div(children=[
                                html.P(children = 'Controversy Level', style={'font-size': '80%'}),
                                html.P(children=level, style={'font-size': '200%', 'font-weight': 'bold'}),
                                html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                            ], style={
                                'width': '50%', 
                                'margin': '5%'
                            }) 
                        ], style = style_widget_kpi)

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
                    ], style={'width': '100%', 'vertical-align': 'middle','font-family': font['helvetica']})
        
        return content
    else:
        content_header_kpi  = html.H3(id = 'content-header', children=['Select a Company'], style={
                                'font-family': font['helvetica'],
                                'font-weight': 'bold', 
                                'margin': '1%'
                            })
        return content_header_kpi