from dash import html

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

#style widget 
#style_widget_news = {
  #  'width': '48%',
  #  'display': 'inline-block',
  #  'vertical-align': 'middle',
  #  'background': colors['background'],
  #  'margin': '1%'

#}

#content-header-news
content_header_news  = html.H3(id = 'content-header',children='Company Experience for ADS.DE WKN: 9389145 / ISIN: NL0000235190', style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            })

#widget-one-news
widget_one_news = html.Div(id = 'news_widget', children =[
                    html.Div(children=[
                        html.H4(id='news_widget_header', children = 'NEWS'),
                        html.P(id='news_widget_text', children='finanzen.net'),
                        html.P(id='kpi_widget_pos', children=['▲'], style={'color': 'green', 'font-size': '80%'})
                    ],style={
                        'width': '50%',
                        'margin': '5%'
                    })
                ])

#widget-two-news
widget_two_news = html.Div(id = 'news_widget', children =[
                    html.Div(children=[
                        html.H5(id='news_widget_header', children = 'MITARBEITER-REVIEWS'),
                        html.P(id='news_widget_text', children='kununu'),
                        html.P(id='news_widget_pos', children=['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%',
                        'margin': '5%'
                    })
                    ])


widget_three_news = html.Div(id = 'news_widget', children =[
                    html.Div(children=[
                        html.P(id='news_widget_header', children = 'ALLE WELT NEWS'),
                        html.P(id='news_widget_text', children='boerse.de'),
                        html.P(id='news_widget_pos', children=['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%',
                        'margin': '5%'
                    })
                    ])

#widget-four-news
widget_four_news = html.Div(id = 'news_widget', children =[
                    html.Div(children=[
                        html.P(id='news_widget_header',children = 'BÖRSENNEWS-FORUM'),
                        html.P(id='news_widget_text',children='boersennews.de/{ISIN}'),
                        html.P(id='news_widget_pos', children=['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })  
                ])

#widget-five-news
widget_five_news = html.Div(id = 'news_widget', children =[
                    html.Div(children=[
                        html.P(id='news_widget_header', children = 'DAX NEWS'),
                        html.P(id='news_widget_text',children='finanzen.net'),
                        html.P(id='news_widget_pos',children=['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ])

#widget-six-news
widget_six_news = html.Div(id = 'news_widget', children =[
                    html.Div(children=[
                        html.P(id='news_widget_header', children = 'KUNDEN'),
                        html.P(id='news_widget_text', children='Trustpilot'),
                        html.P(id='news_widget_pos',children=['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ])
