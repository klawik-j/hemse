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
    id="output-message-activity-form",
    is_open=False,
    dismissable=True,
    duration=2000,
    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
activity_type_input = html.Div(
    children=[
        dbc.Label("type"),
        dbc.Select(
            id="select-activity-type",
            options=[
                "running",
                "swimming",
                "gym",
                "skating",
                "other",
            ],
            style={"background-color": Color.primary, "color": Color.text},
        ),
    ],
)
value_type_input = html.Div(
    children=[
        dbc.Label("value"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("km"),
                dbc.Input(
                    id="activity-value",
                    type="number",
                    min=0,
                    value=0,
                    style={
                        "background-color": Color.primary,
                        "color": Color.text,
                        "-moz-appearance": "textfield",
                        "appearance": "textfield",
                    },
                ),
            ],
        ),
    ]
)
duration_type_input = html.Div(
    children=[
        dbc.Label("duration"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("min"),
                dbc.Input(
                    id="activity-duration-min",
                    type="number",
                    min=0,
                    value=30,
                    style={
                        "background-color": Color.primary,
                        "color": Color.text,
                        "-moz-appearance": "textfield",
                        "appearance": "textfield",
                    },
                ),
                dbc.InputGroupText("s"),
                dbc.Input(
                    id="activity-duration-s",
                    type="number",
                    min=0,
                    max=60,
                    value=0,
                    style={
                        "background-color": Color.primary,
                        "color": Color.text,
                        "-moz-appearance": "textfield",
                        "appearance": "textfield",
                    },
                ),
            ],
        ),
    ]
)

form = dbc.Card(
    [
        dbc.Row(user_input, className="mb-3"),
        dbc.Row(activity_type_input, className="mb-3"),
        dbc.Row(value_type_input, className="mb-3"),
        dbc.Row(duration_type_input, className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    date_input,
                ),
                dbc.Col(
                    dbc.Button(
                        "Submit", id="submit-button-activity-form", color="primary"
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
