from datetime import datetime
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from src.common.color import Color

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
    className="mb-3",
)
weight_input = html.Div(
    children=[
        dbc.Label("weight"),
        dbc.Input(
            id="weight-value",
            type="number",
            min=0,
            placeholder="weight",
            style={"background-color": Color.primary, "color": Color.text},
        ),
    ],
    className="mb-3",
)
date_input = html.Div(
    children=[
        dcc.DatePickerSingle(
            id="date-picker",
            date=datetime.today(),
            display_format="YYYY-MM-DD",
        ),
    ],
    className="mb-3",
)
return_info = dbc.Toast(
    "This toast is placed in the top right",
    id="output-message-weight-form",
    is_open=False,
    dismissable=True,
    duration=2000,
    # top: 66 positions the toast below the navbar
    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)

form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(user_input, className="me-3", width="auto"),
                dbc.Col(weight_input, className="me-3", width="auto"),
            ],
            className="g-2",
        ),
        dbc.Row(
            [
                dbc.Col(date_input, className="me-3", width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Submit", id="submit-button-weight-form", color="primary"
                    ),
                    width="auto",
                ),
            ],
            className="g-2",
        ),
    ],
)

layout = html.Div(
    children=[form, return_info],
    style={
        "background-color": Color.secondary,
        "border-radius": "10px",
        "padding": "20px",
    },
    className="col-md-6 mx-auto my-4 mt-4",
)
