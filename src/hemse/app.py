import json
import os
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
from dash import dcc, html
from dash.dependencies import Input, Output, State

from hemse.common.color import Color


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
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    use_pages=True,
)
server = app.server


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                html.I(className="bi bi-github"),
                href="https://github.com/klawik-j/hemse/",
                target="_blank",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                ["add weight"],
                href=dash.page_registry["pages.add_weight"]["path"],
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                ["add activity"],
                href=dash.page_registry["pages.add_activity"]["path"],
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                ["telemetry"],
                href=dash.page_registry["pages.telemetry"]["path"],
            )
        ),
    ],
    brand="hemse",
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


@app.callback(
    Output("measurement-chart", "figure"),
    [
        Input("select-user", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_chart(selected_user_id, n_intervals):
    measurements = get_measurements(user_id=selected_user_id, type="weight")
    dates = [measurement["created_at"] for measurement in measurements]
    values = [measurement["value"] for measurement in measurements]
    return {
        "data": [
            {
                "x": dates,
                "y": values,
                "type": "line",
            }
        ],
        "layout": {
            "margin": dict(l=20, r=20, t=20, b=20),
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "white"},
            "autosize": True,
        },
    }


@app.callback(
    Output("heatmap", "figure"),
    [
        Input("select-user", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_heatmap_data(user_id, n_intervals):
    activities = get_activities(user_id=user_id)

    current_year = datetime.now().year
    current_week = datetime.now().isocalendar().week
    weeks = range(1, current_week + 1)

    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    matrix = [[0] * 7 for _ in weeks]
    for activity in activities:
        date = activity["created_at"]
        if date.year != current_year:
            break
        week = date.isocalendar().week - 1
        day_of_week = date.weekday()
        matrix[week][day_of_week] += 1

    figure = go.Figure(
        data=[
            go.Heatmap(
                z=matrix,
                y=[f"week {i}" for i in weeks],
                x=days_of_week,
                colorscale=[[0, Color.secondary], [1, Color.third]],
                hoverongaps=False,
                showlegend=False,
                showscale=False,
                zauto=False,
                zmax=1,
                zmin=0,
                xgap=4,
                ygap=4,
            )
        ],
        layout=go.Layout(
            yaxis=dict(scaleanchor="x", gridcolor="rgba(0, 0, 0, 0)"),
            xaxis=dict(gridcolor="rgba(0, 0, 0, 0)"),
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
        ),
    )
    return figure


@app.callback(
    Output("activity_type_pie_chart", "figure"),
    [
        Input("select-user", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_activity_type_pie_chart(user_id, n_intervals):
    activities = get_activities(user_id=user_id)
    data = {}
    for activity in activities:
        activity_type = activity["type"]
        data[activity_type] = data.get(activity_type, 0) + 1
    activity_types = list(data.keys())
    activity_counts = [data[activity_type] for activity_type in activity_types]

    figure = go.Figure(
        data=[
            go.Pie(
                labels=activity_types,
                values=activity_counts,
                hole=0.4,
                textinfo="label+value",
                showlegend=False,
                marker=dict(colors=Color.chart),
            )
        ],
        layout=go.Layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
        ),
    )

    return figure


@app.callback(
    Output("activity-counter", "children"),
    [
        Input("select-user", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_activity_counter(user_id, n_clicks):
    return [len(get_activities(user_id=user_id))]


# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
