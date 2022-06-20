import dash
from dash import html, dcc

# import .sidebar as sb

dash.register_page(__name__,
    path="/Home",
    title="Home",
    name="Home",)

layout = html.Div(
    children=[
        html.H1(children="This is our home page"),
        # sb.sidebar,
        html.Div(
            children="""
        This is our home page content.
    """
        ),
    ]
)
