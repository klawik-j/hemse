import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objs as go
from dash import dcc, html

from hemse.common.color import Color

dash.register_page(__name__)

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

form = dbc.Card(
    [
        dbc.Row(user_input, className="mb-3"),
    ],
    style={
        "background-color": Color.secondary,
        "border-radius": "10px",
        "padding": "20px",
    },
    body=True,
)

weight_graph = dbc.Card(
    [
        dbc.Row(
            dcc.Graph(
                id="measurement-chart",
                style={"background-color": Color.primary, "color": Color.text},
                config={
                    "displayModeBar": False,
                    "scrollZoom": False,
                    "staticPlot": True,
                },
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

activity_counter = dbc.Card(
    [
        dbc.Row(
            html.Div(
                id="activity-counter",
                children=[],
                style={
                    "textAlign": "center",
                    "background-color": Color.primary,
                    "color": Color.third,
                    "fontSize": "8em",
                },
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

activity_heatmap = dbc.Card(
    [
        dcc.Graph(
            id="heatmap",
            figure=go.Figure(),
            config={
                "displayModeBar": False,
                "staticPlot": True,
            },
            style={
                "background-color": Color.primary,
                "color": Color.text,
            },
        ),
    ],
    style={
        "background-color": Color.secondary,
        "border-radius": "10px",
        "padding": "20px",
    },
    body=True,
)

activity_type_pie_chart = dbc.Card(
    [
        dcc.Graph(
            id="activity_type_pie_chart",
            figure=go.Figure(),
            config={
                "displayModeBar": False,
                "staticPlot": True,
            },
            style={
                "background-color": Color.primary,
                "color": Color.text,
            },
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
                        dbc.Col(form, md=3),
                    ],
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(activity_counter, md=3),
                    ],
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(activity_heatmap, md=3),
                    ],
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(activity_type_pie_chart, md=3),
                    ],
                    align="center",
                ),
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
