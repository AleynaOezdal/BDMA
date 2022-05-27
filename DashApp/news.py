from dash import html
from retrieve_sample_data import get_stocks_data, get_news_data, get_kpi_data


colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

#style widget 
style_widget_news = {
    'width': '48%', 
    'display': 'inline-block', 
    'vertical-align': 'middle', 
    'background': colors['background'], 
    'margin': '1%'

}

#content-header-news
content_header_news  = html.H3(id = 'content-header',children='News for ADS.DE', style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            })

#widget-one-news
widget_one_news = html.Div(id = 'widget-one', children =[
                    html.Div(children=[
                        html.H4(children = 'NEWS', style={'font-size': '100%'}),
                        html.P(children='yfinance oder finanzen.net', style={'font-size': '80%'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '40%', 
                        'margin': '5%',
                        'display': 'inline-block'
                    })
                ], style=style_widget_news)

#widget-two-news
widget_two_news = html.Div(id = 'widget-two', children =[
                    html.Div(children=[
                        html.P(children = 'MITARBEITER-REVIEWS', style={'font-size': '100%'}),
                        html.P(children='kununu oder glasdoor', style={'font-size': '80%'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style=style_widget_news)

#widget-four-news
widget_four_news = html.Div(id = 'widget-four', children =[
                    html.Div(children=[
                        html.P(children = 'BRANCHENNEWS', style={'font-size': '100%'}),
                        html.P(children='finanzen.net oder boerse.de', style={'font-size': '80%'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })  
                ], style=style_widget_news)

#widget-five-news
widget_five_news = html.Div(id = 'widget-five', children =[
                    html.Div(children=[
                        html.P(children = 'GLOBALE NEWS', style={'font-size': '100%'}),
                        html.P(children='finanzen.net', style={'font-size': '80%'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style=style_widget_news)

#widget-six-news
widget_six_news = html.Div(id = 'widget-six', children =[
                    html.Div(children=[
                        html.P(children = 'KUNDEN', style={'font-size': '100%'}),
                        html.P(children='tbd', style={'font-size': '80%'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style=style_widget_news)
