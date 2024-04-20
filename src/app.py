# Import packages
from datetime import datetime

import requests
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


def get_users():
    url = "http://localhost:8000/api/users/"
    params = {"skip": 0, "limit": 100}
    headers = {"accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_measurements():
    url = "http://localhost:8000/api/measurements/"
    params = {"skip": 0, "limit": 100}
    headers = {"accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


weight_data = get_measurements()
user_data = get_users()

# Convert created_at strings to datetime objects
for entry in weight_data:
    entry["created_at"] = datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%S.%f")

# Sort the weight data by created_at timestamps
weight_data = sorted(weight_data, key=lambda x: x["created_at"])

# Define a Dash application instance
app = Dash(__name__)

# Define the layout of the application
app.layout = html.Div(
    children=[
        html.H1(children="Measurement Over Time"),
        html.Label("Select User:"),
        dcc.Dropdown(
            id="user-dropdown",
            options=[
                {"label": user["name"], "value": user["user_id"]} for user in user_data
            ],
            value=user_data[0]["user_id"],
        ),
        html.Label("Select Type:"),
        dcc.Dropdown(
            id="type-dropdown",
            options=[
                {"label": type_, "value": type_}
                for type_ in set(entry["type"] for entry in weight_data)
            ],
            value=weight_data[0]["type"],
        ),
        dcc.Graph(id="measurement-chart"),
    ]
)


# Define a callback to update the chart based on the selected user and type
@app.callback(
    Output("measurement-chart", "figure"),
    [Input("user-dropdown", "value"), Input("type-dropdown", "value")],
)
def update_chart(selected_user_id, selected_type):
    filtered_data = [
        entry
        for entry in weight_data
        if entry["user_id"] == selected_user_id and entry["type"] == selected_type
    ]
    dates = [entry["created_at"] for entry in filtered_data]
    values = [entry["value"] for entry in filtered_data]

    return {
        "data": [
            {
                "x": dates,
                "y": values,
                "type": "line",
                "name": f'{selected_type.capitalize()} ({next(user["name"] for user in user_data if user["user_id"] == selected_user_id)})',    # noqa: E501
            }
        ],
        "layout": {
            "title": f'{selected_type.capitalize()} Over Time ({next(user["name"] for user in user_data if user["user_id"] == selected_user_id)})', # noqa: E501
            "xaxis": {"title": "Date"},
            "yaxis": {"title": selected_type.capitalize()},
        },
    }

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
    