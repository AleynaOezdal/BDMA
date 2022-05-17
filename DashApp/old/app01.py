from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#F6F6F6'
}

font = {
    'helvetica' : 'Arial, Helvetica, sans-serif'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

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

#▼

# app layout
app.layout = html.Div( children=[
    html.H1(id = 'Header',
        children='Dashboard', style={
        'font-family': font['helvetica']
    }
    ),
    html.Div(children='Good morning, Mr. CEO.', style={
        'font-family': font['helvetica']
    }),
    html.Div(children='Team Dashboard wishes you a sucessful day with right decisions!', style={
        'font-family': font['helvetica']
        
    }),
    html.Div(id = 'Side',children= [
        html.Div(id = 'navigation',children=[
            dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
            html.Div(id='dd-output-container')
        ], style = {'width': '30%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'height': 600}),
        html.Div(id = 'content', children=[
            html.H3(id = 'content-header',children='Key Performance Indicators for ADS.DE', style={
                'font-family': font['helvetica'],
                'font-weight': 'bold', 
                'margin': '1%'
            }),
            html.Div(id = 'widget', children = [ 
                html.Div(id = 'widget-one', children =[
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
                ], style={'width': '48%' , 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'}),
                html.Div(id = 'widget-two', children =[
                    html.Div(children=[
                        html.P(children = 'EBITDA in MEUR', style={'font-size': '80%'}),
                        html.P(children='3,178', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'}),
                html.Div(id = 'widget-three', children =[
                    html.Div(children=[
                        html.P(children = 'Profit Margin in %', style={'font-size': '80%'}),
                        html.P(children='9,97', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'}),
                html.Div(id = 'widget-four', children =[
                    html.Div(children=[
                        html.P(children = 'ESG Risk Score', style={'font-size': '80%'}),
                        html.P(children='13', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })  
                ], style={'width': '48%' , 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'}),
                html.Div(id = 'widget-five', children =[
                    html.Div(children=[
                        html.P(children = 'Revenue in MEUR', style={'font-size': '80%'}),
                        html.P(children='21,230,000', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    })   
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'}),
                html.Div(id = 'widget-six', children =[
                    html.Div(children=[
                        html.P(children = 'Controversy Level', style={'font-size': '80%'}),
                        html.P(children='3', style={'font-size': '200%', 'font-weight': 'bold'}),
                        html.P(['▲'], style={'color': 'green', 'font-size': '80%'})
                    ], style={
                        'width': '50%', 
                        'margin': '5%'
                    }) 
                ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'middle', 'background': colors['background'], 'margin': '1%'}),
            ])
        ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'middle','font-family': font['helvetica']})
    ]),   
])

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)

def update_output(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=True)