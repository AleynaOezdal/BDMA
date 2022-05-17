from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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

df2 = pd.read_csv(
    'https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

#header
header = html.Div(id = 'Header', children= [
    html.H1(children='Dashboard', style={
        'font-family': font['helvetica']
    }
    ),
    html.Div(children='Good morning, Mr. CEO.', style={
        'font-family': font['helvetica']
    }),
    html.Div(children='Team Dashboard wishes you a sucessful day with right decisions!', style={
        'font-family': font['helvetica']
        
    })])

#navigation/sidebar
sidebar = html.Div(id = 'navigation',children=[
            html.P(
                'Here you can Search'
            ),

            html.Div(dcc.Input(id='input-box1', placeholder='Select DAX-Company', type='text')),
            #absatz
            html.Br(),
            html.Div(dcc.Input(id='input-box2', placeholder='Select Time', type='text')),
            html.Br(),
            html.Button('Submit', id='button-example-1'),
            html.Div(id='output-container-button',
                    children='Enter a value and press submit'),
            html.Br(),
            dbc.Nav(
                [
                    dbc.NavLink("KPI's", href="/KPI's", active='exact'),
                    dbc.NavLink('Stocks', href='/Stocks', active='exact'),
                    dbc.NavLink('News', href='/News', active='exact'),
                ],
                vertical=True,
                pills=True,
            ),
                html.H4(
                'Quote of the Day:'
                ),
                html.P(
                'Every new day begins with possibilities'
                ),
        ], style = {'width': '30%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'top': 0, 'left': 0, 'bottom': 0, 'padding': '2rem 1rem'})

# content-header
content_header  = html.H3(id = 'content-header',children='Key Performance Indicators for ADS.DE', style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            })

#widget-one
widget_one = html.Div(id = 'widget-one', children =[
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
                    )],style={'width': '40%' , 'display': 'inline-block', 'margin': '5%'})  
                ], style={'width': '48%' , 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'})

#widget-two
widget_two = html.Div(id = 'widget-two', children =[
                    html.Div(children=[
                        html.P(children = 'EBITDA in MEUR', style={'font-size': '80%'}),
                        html.P(children='3,178', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'})

#widget-three
widget_three = html.Div(id = 'widget-three', children =[
                    html.Div(children=[
                    html.P(children = 'Profit Margin in %', style={'font-size': '80%'}),
                    html.P(children='9,97', style={'font-size': '200%', 'font-weight': 'bold'}),
                    html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'})

#widget-four
widget_four = html.Div(id = 'widget-four', children =[
                    html.Div(children=[
                        html.P(children = 'ESG Risk Score', style={'font-size': '80%'}),
                        html.P(children='13', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })  
                ], style={'width': '48%' , 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'})

#widget-five
widget_five = html.Div(id = 'widget-five', children =[
                    html.Div(children=[
                        html.P(children = 'Revenue in MEUR', style={'font-size': '80%'}),
                        html.P(children='21,230,000', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'})

#widget-six
widget_six = html.Div(id = 'widget-six', children =[
                    html.Div(children=[
                        html.P(children = 'Controversy Level', style={'font-size': '80%'}),
                        html.P(children='3', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'})

#content
content = html.Div(id = 'content', children=[
                content_header,
                html.Div(id = 'widget', children = [ 
                    widget_one,
                    widget_two,
                    widget_three,
                    widget_four,
                    widget_five,
                    widget_six,
                ])
            ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})

#side posiblilitis 
def render_page_content(pathname):
    if pathname == "/KPI's":
        return [
            html.Div(id = 'content', children=[
                content_header,
                html.Div(id = 'widget', children = [ 
                    widget_one,
                    widget_two,
                    widget_three,
                    widget_four,
                    widget_five,
                    widget_six,
                ])
            ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})
        ]
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
            html.H1('News for ADS.DE',
                    style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            }),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df2, barmode='group', x='Years',
                                    y=['Girls High School', 'Boys High School']))
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1('404: Not found', className='text-danger'),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognised...'),
        ]
    )

#▼

# app layout
app.layout = html.Div( children=[
    header,
    html.Div(id = 'Side',children= [
        dcc.Location(id='url'),
        sidebar,
        content
    ]),   
])

@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)

@app.callback(
    Output('output-container-button', 'children'),
    Input('button-example-1', 'n_clicks'),
    State('input-box1', 'value'))

def update_output(n_clicks, value):
    return ''.format(
        value,
        n_clicks
    )

if __name__ == '__main__':
    app.run_server(debug=True)