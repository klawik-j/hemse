import dash
from dash import Input, Output, callback, dcc, html

dash.register_page(__name__, path="/")

layout = html.Div(children=[html.Div(children="home")])
