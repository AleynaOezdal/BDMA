from dash import dcc, html
import plotly.express as px
import pandas as pd
from retrieve_sample_data import get_stocks_data, get_news_data, get_kpi_data

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

#content-header-kpi
content_header_kpi  = html.H3(id = 'content-header',children='Key Performance Indicators for ADS.DE', style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            })

#widget-one-kpi
widget_one_kpi = html.Div(id = 'widget-one', children =[
                    html.Div(children=[
                        html.P(children = 'Free Cashflow in MEUR', style={'font-size': '80%'}),
                        html.P(children='2,525', style={'font-size': '200%', 'font-weight': 'bold'}),
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

#widget-two-kpi
widget_two_kpi = html.Div(id = 'widget-two', children =[
                    html.Div(children=[
                        html.P(children = 'EBITDA in MEUR', style={'font-size': '80%'}),
                        html.P(children='3,178', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style = style_widget_kpi)

#widget-three-kpi
widget_three_kpi = html.Div(id = 'widget-three', children =[
                    html.Div(children=[
                    html.P(children = 'Profit Margin in %', style={'font-size': '80%'}),
                    html.P(children='9,97', style={'font-size': '200%', 'font-weight': 'bold'}),
                    html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style = style_widget_kpi)

#widget-four-kpi
widget_four_kpi = html.Div(id = 'widget-four', children =[
                    html.Div(children=[
                        html.P(children = 'ESG Risk Score', style={'font-size': '80%'}),
                        html.P(children='13', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })  
                ], style = style_widget_kpi)

#widget-five-kpi
widget_five_kpi = html.Div(id = 'widget-five', children =[
                    html.Div(children=[
                        html.P(children = 'Revenue in MEUR', style={'font-size': '80%'}),
                        html.P(children='21,230,000', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style = style_widget_kpi)

#widget-six-kpi
widget_six_kpi = html.Div(id = 'widget-six', children =[
                    html.Div(children=[
                        html.P(children = 'Controversy Level', style={'font-size': '80%'}),
                        html.P(children='3', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style = style_widget_kpi)