import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dcc, html

from src.common.color import Color

dash.register_page(__name__)

# Sample data
x_values = [1, 2, 3, 4, 5]
y_values = [10, 11, 12, 13, 14]


# Define styles
header_style = {"backgroundColor": "blue", "color": "white"}
graph_style = {"backgroundColor": "lightgrey"}

user_input = html.Div(
    children=[
        dbc.Label("user"),
        dbc.Select(
            id="select-user",
            value=1,
            style={"background-color": Color.primary, "color": Color.text},
        ),
    ],
)

weight_graph = dbc.Card(
    [
        dbc.Row(user_input, className="mb-3"),
        dbc.Row(
            dcc.Graph(
                id="measurement-chart",
                style={"background-color": Color.primary, "color": Color.text},
                config={"displayModeBar": False, "scrollZoom": False},
            ),
            className="mb-3",
        ),
    ],
    style={
        "background-color": Color.secondary,
        "border-radius": "10px",
        "padding": "20px",
    },
    body=True,
)

layout = html.Div(
    children=[
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(weight_graph, md=8),
                    ],
                    align="center",
                ),
            ],
            fluid=True,
        ),
    ],
)
