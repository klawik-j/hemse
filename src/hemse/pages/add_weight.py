from datetime import datetime

import dash
import dash_bootstrap_components as dbc
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
weight_input = html.Div(
    children=[
        dbc.Label("weight"),
        dbc.Input(
            id="weight-value",
            type="number",
            min=0,
            placeholder="kg",
            style={
                "background-color": Color.primary,
                "color": Color.text,
                "-moz-appearance": "textfield",
                "appearance": "textfield",
            },
        ),
    ],
)
date_input = html.Div(
    children=[
        dcc.DatePickerSingle(
            id="date-picker",
            date=datetime.today(),
            display_format="YYYY-MM-DD",
        ),
    ],
)
return_info = dbc.Toast(
    "",
    id="output-message-weight-form",
    is_open=False,
    dismissable=True,
    duration=2000,
    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)

form = dbc.Card(
    [
        dbc.Row(user_input, className="mb-3"),
        dbc.Row(weight_input, className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    date_input,
                ),
                dbc.Col(
                    dbc.Button(
                        "Submit", id="submit-button-weight-form", color="primary"
                    ),
                ),
            ],
            className="g-2",
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
            ],
            fluid=True,
        ),
        return_info,
    ],
)
