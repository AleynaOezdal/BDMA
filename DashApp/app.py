from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sidebar as sb
import kpi
import news

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

#header
header = html.Div(id = 'Header', children= [
    html.H1(children='DAX40 - das Unternehmer-Dashboard'),
    html.Div(children='Guten Tag Herr. CEO.'),
    html.Div(children='Team DAX40 wünscht Ihnen einen erfolgreichen Tag mit richtigen Entscheidungen!')])

#content
content = html.Div(id = 'page_content', children=[])

#▼

#overview
def overview(value):
    overview_content = html.Div(id = 'content', children=[
                            kpi.get_value_without_kpi(value),
                            html.Div(id = 'widget', children = [])])
    return overview_content

# app layout
app.layout = html.Div( children=[
    header,
    html.Div(id = 'side',children= [
        dcc.Location(id='url'),
        sb.sidebar,
        content
    ]),   
])

@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname'),
    Input('button_search', 'n_clicks'),
    State('dropdown', 'value')
)

#side posiblilitis 
def render_page_content(pathname, n_clicks, value):
    if n_clicks is None:
        return [overview(value)]
    else:
        if pathname == '/':
            return [overview(value)]
        elif pathname == "/Keyperformance":
            return [kpi.get_kpi_content_value(value)]
        elif pathname == '/Investorrelations':
            return [
                html.H3('Investor Relations for ADS.DE WKN: 9389145 / ISIN: NL0000235190',
                        style={
                   'font-family': font['helvetica'],
                   'font-weight': 'bold',
                   'margin': '1%'
                })
            ]
        elif pathname == '/Companyexperience':
            return [
                html.Div(id = 'content_news', children=[
                    news.content_header_news,
                    html.Div(id = 'widget_news', children = [ 
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
    app.run_server(debug=True)