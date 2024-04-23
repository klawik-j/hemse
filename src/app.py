import json
import os
from datetime import datetime

import dash
import requests
from dash import dcc, html
from dash.dependencies import Input, Output, State


def get_users(**kwags):
    url = os.environ["BACKEND_URL"] + "/api/users/"
    params = {"skip": 0, "limit": 100} | kwags
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_measurements(**kwags):
    url = os.environ["BACKEND_URL"] + "/api/measurements/"
    params = {"skip": 0, "limit": 100} | kwags
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    for entry in data:
        entry["created_at"] = datetime.strptime(
            entry["created_at"], "%Y-%m-%dT%H:%M:%S"
        )
    return sorted(data, key=lambda x: x["created_at"])


# Define Dash application instance
app = dash.Dash(__name__)
server = app.server

# Define layout of the application
app.layout = html.Div(
    [
        html.H1("Wakacje sa"),
        html.Div(
            [
                html.H2(children="Add weight"),
                html.Label("Select User:"),
                dcc.Dropdown(id="user-dropdown-form"),
                html.Label("Weight:"),
                dcc.Input(
                    id="measurment-value",
                    type="number",
                    placeholder="ile tam na wadze byczqu ?",
                ),
                html.Label("Date:"),
                dcc.DatePickerSingle(
                    id="date-picker", date=datetime.today(), display_format="YYYY-MM-DD"
                ),
                html.Button("Submit", id="submit-button-form", n_clicks=0),
                dcc.Interval(
                    id="interval-component-form", interval=30000, n_intervals=1
                ),
                html.Div(id="output-message-form"),
            ]
        ),
        html.Div(
            [
                html.H2(children="Weight Over Time"),
                html.Label("Select User:"),
                dcc.Dropdown(id="user-dropdown", value=1),
                html.Label("Select Type:"),
                dcc.Dropdown(id="type-dropdown", value="weight"),
                dcc.Graph(id="measurement-chart"),
                dcc.Interval(id="interval-component", interval=30000, n_intervals=1),
            ]
        ),
    ]
)


@app.callback(
    Output("output-message-form", "children"),
    Input("submit-button-form", "n_clicks"),
    [
        State("measurment-value", "value"),
        State("date-picker", "date"),
        State("user-dropdown-form", "value"),
    ],
)
def measurement_form(n_clicks, measurment_value, date_picker, user_dropdown_form):
    if (
        measurment_value is None
        or date_picker is None
        or user_dropdown_form is None
        or n_clicks is None
    ):
        return ""
    url = os.environ["BACKEND_URL"] + "/api/measurements/"
    data = json.dumps(
        {
            "type": "weight",
            "value": measurment_value,
            "user_id": user_dropdown_form,
            "created_at": date_picker,
        }
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        return "Created !"
    else:
        return "Failure"


@app.callback(
    Output("user-dropdown-form", "options"),
    [Input("interval-component", "n_intervals")],
)
def update_users_dropdown_form(n_intervals):
    users = get_users()
    return [
        {
            "label": user["name"],
            "value": user["user_id"],
        }
        for user in users
    ]


# ----------------------------------------


@app.callback(
    Output("user-dropdown", "options"), [Input("interval-component", "n_intervals")]
)
def update_users_dropdown(n_intervals):
    users = get_users()
    return [
        {
            "label": user["name"],
            "value": user["user_id"],
        }
        for user in users
    ]


@app.callback(
    Output("type-dropdown", "options"), [Input("interval-component", "n_intervals")]
)
def update_types_dropdown(n_intervals):
    return [{"label": "weight", "value": "weight"}]


@app.callback(
    Output("measurement-chart", "figure"),
    [
        Input("user-dropdown", "value"),
        Input("type-dropdown", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_chart(selected_user_id, selected_type, n_intervals):
    user_name = get_users(user_id=selected_user_id)[0]["name"]
    measurements = get_measurements(user_id=selected_user_id, type=selected_type)
    dates = [measurement["created_at"] for measurement in measurements]
    values = [measurement["value"] for measurement in measurements]
    return {
        "data": [
            {
                "x": dates,
                "y": values,
                "type": "line",
                "name": f"{selected_type.capitalize()} ({user_name})",
            }
        ],
        "layout": {
            "title": f"{selected_type.capitalize()} Over Time ({user_name})",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": selected_type.capitalize()},
        },
    }


# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
