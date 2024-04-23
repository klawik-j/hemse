import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
import os
import requests

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
        entry["created_at"] = datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
    return sorted(data, key=lambda x: x["created_at"])

# Define Dash application instance
app = dash.Dash(__name__)
server = app.server

# Define layout of the application
app.layout = html.Div(
    children=[
        html.H1(children="Measurement Over Time"),
        html.Label("Select User:"),
        dcc.Dropdown(id="user-dropdown", value=1),
        html.Label("Select Type:"),
        dcc.Dropdown(id="type-dropdown", value="weight"),
        dcc.Graph(id="measurement-chart"),
        dcc.Interval(id='interval-component', interval=30000, n_intervals=1)  # Set n_intervals to 1
    ]
)

@app.callback(
    Output("user-dropdown", "options"),
    [Input("interval-component", "n_intervals")]
)
def update_users_dropdown(n_intervals):
    users = get_users()
    return [{"label": user["name"], "value": user["user_id"], } for user in users]

@app.callback(
    Output("type-dropdown", "options"),
    [Input("interval-component", "n_intervals")]
)
def update_types_dropdown(n_intervals):
    return [{"label": "weight", "value": "weight"}]

@app.callback(
    Output("measurement-chart", "figure"),
    [Input("user-dropdown", "value"), Input("type-dropdown", "value"), Input("interval-component", "n_intervals")]
)
def update_chart(selected_user_id, selected_type, n_intervals):
    user_name = get_users(user_id=selected_user_id)[0]["name"]
    measurements = get_measurements(user_id = selected_user_id, type = selected_type)
    dates = [measurement["created_at"] for measurement in measurements]
    values = [measurement["value"] for measurement in measurements]
    return {
        "data": [
            {
                "x": dates,
                "y": values,
                "type": "line",
                "name": f'{selected_type.capitalize()} ({user_name})',
            }
        ],
        "layout": {
            "title": f'{selected_type.capitalize()} Over Time ({user_name})',
            "xaxis": {"title": "Date"},
            "yaxis": {"title": selected_type.capitalize()},
        },
    }

# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
