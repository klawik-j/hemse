import json
import os
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import requests
from dash import dcc, html
from dash.dependencies import Input, Output, State


def get_users(**kwargs):
    url = os.environ["BACKEND_URL"] + "/api/users/"
    params = {"skip": 0, "limit": 100} | kwargs
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_measurements(**kwargs):
    url = os.environ["BACKEND_URL"] + "/api/measurements/"
    params = {"skip": 0, "limit": 100} | kwargs
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    for entry in data:
        entry["created_at"] = datetime.strptime(
            entry["created_at"], "%Y-%m-%dT%H:%M:%S"
        )
    return sorted(data, key=lambda x: x["created_at"])


def get_activities(**kwargs):
    url = os.environ["BACKEND_URL"] + "/api/activities/"
    params = {"skip": 0, "limit": 100} | kwargs
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], use_pages=True)
server = app.server


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                "add weight", href=dash.page_registry["pages.add_weight"]["path"]
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "add activity", href=dash.page_registry["pages.add_activity"]["path"]
            )
        ),
        dbc.NavItem(
            dbc.NavLink("telemetry", href=dash.page_registry["pages.telemetry"]["path"])
        ),
    ],
    brand="JebacUlaneKurwy",
    brand_href=dash.page_registry["pages.home"]["path"],
    color="primary",
    dark=True,
)

app.layout = html.Div(
    children=[
        html.Div(children=[navbar]),
        dash.page_container,
        dcc.Interval(id="interval-component", interval=30000, n_intervals=1),
    ],
)


@app.callback(
    Output("select-user", "options"),
    [Input("interval-component", "n_intervals")],
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
    Output("output-message-weight-form", "children"),
    Output("output-message-weight-form", "is_open"),
    Output("output-message-weight-form", "icon"),
    Input("submit-button-weight-form", "n_clicks"),
    [
        State("weight-value", "value"),
        State("date-picker", "date"),
        State("select-user", "value"),
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
        return ["Created !", True, "success"]
    else:
        return ["Failure", True, "danger"]


@app.callback(
    Output("output-message-activity-form", "children"),
    Output("output-message-activity-form", "is_open"),
    Output("output-message-activity-form", "icon"),
    Input("submit-button-activity-form", "n_clicks"),
    [
        State("date-picker", "date"),
        State("select-user", "value"),
        State("select-activity-type", "value"),
        State("activity-value", "value"),
        State("activity-duration-min", "value"),
        State("activity-duration-s", "value"),
    ],
)
def activity_form(
    n_clicks,
    date_picker,
    user_dropdown_form,
    select_activity_type,
    activity_value,
    activity_duration_min,
    activity_duration_s,
):
    if (
        select_activity_type is None
        or date_picker is None
        or user_dropdown_form is None
        or activity_value is None
        or activity_duration_min is None
        or activity_duration_s is None
        or n_clicks is None
    ):
        return ""
    url = os.environ["BACKEND_URL"] + "/api/activities/"
    data = json.dumps(
        {
            "type": select_activity_type,
            "value": activity_value,
            "duration": f"PT{activity_duration_min}M{activity_duration_s}S",
            "user_id": user_dropdown_form,
            "created_at": date_picker,
        }
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return ["Created !", True, "success"]
    else:
        return ["Failure", True, "danger"]


# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
