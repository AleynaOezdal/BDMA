from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sidebar as sb
import kpi
import news
from retrieve_sample_data import get_stocks_data, get_news_data, get_kpi_data

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

df2 = pd.read_csv(
    'https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

#header
header = html.Div(id = 'Header', children= [
    html.H1(children='Dashboard', style={
        #'font-family': font['helvetica'],
        'font-weight': 'bold'
    }
    ),
    html.Div(children='Good morning, Mr. CEO.', style={
        'font-family': font['helvetica']
    }),
    html.Div(children='Team Dashboard wishes you a sucessful day with right decisions!', style={
        'font-family': font['helvetica']
        
    })], style = {'padding': '1%'})

#content
content = html.Div(id = 'page_content', children=[], style={'width': '75%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})

#▼

#kpi content 
def kpi_content_get():
    kpi_content = html.Div(id = 'content', children=[
                    kpi.content_header_kpi,
                    html.Div(id = 'widget', children = [ 
                        kpi.widget_one_kpi,
                        kpi.widget_two_kpi,
                        kpi.widget_three_kpi,
                        kpi.widget_four_kpi,
                        kpi.widget_five_kpi,
                        kpi.widget_six_kpi,
                    ])
                ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})
    return kpi_content

#overview
def overview(value):
    overview_content = html.Div(id = 'content', children=[
                            kpi.get_value_without_kpi(value),
                            html.Div(id = 'widget', children = [])
                        ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})
    return overview_content

# app layout
app.layout = html.Div( children=[
    header,
    html.Div(id = 'Side',children= [
        dcc.Location(id='url'),
        sb.sidebar,
        content
    ], style = {'padding': '1%', 'display': 'flex'}),   
])

@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname'),
    Input('button-example-1', 'n_clicks'),
    State('demo-dropdown', 'value')
)

#side posiblilitis 
def render_page_content(pathname, n_clicks, value):
    if n_clicks is None:
        return [overview(value)]
    else:
        if pathname == '/':
            return [overview(value)]
        elif pathname == "/KPI's":
            return [kpi.get_kpi_content_value(value)]
        elif pathname == '/Stocks':
            return [
                html.H1('Stocks for ADS.DE',
                        style={
                    'font-family': font['helvetica'],
                    'font-weight': 'bold', 
                    'margin': '1%'
                }),
                dcc.Graph(id='bargraph',
                        figure=px.bar(df2, barmode='group', x='Years',
                                        y=['Girls Grade School', 'Boys Grade School']))
            ]
        elif pathname == '/News':
            return [
                html.Div(id = 'content', children=[
                    news.content_header_news,
                    html.Div(id = 'widget', children = [ 
                        news.widget_one_news,
                        news.widget_two_news,
                        news.widget_three_news,
                        news.widget_four_news,
                        news.widget_five_news,
                        news.widget_six_news,
                    ])
                ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})
            ]
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1('404: Not found', className='text-danger'),
                html.Hr(),
                html.P(f'The pathname {pathname} was not recognised...'),
            ]
        )

if __name__ == '__main__':
    app.run_server(debug=True),