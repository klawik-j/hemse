import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path="/")

layout = html.Div(children=[html.Div(children="home")])
