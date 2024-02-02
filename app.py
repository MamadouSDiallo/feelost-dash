# Import packages

import dash
from dash import Dash, html, dcc
import dash_auth
import dash_bootstrap_components as dbc

# from script.datasets import datasets_fe, datasets_be

from env.secrets import VALID_USERNAME_PASSWORD_PAIRS


# Initialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.title = "FeeLoST"

nav_menu = dbc.Nav(
    id="nav-bar",
    children=[
        dbc.NavLink(children="About FeeLoST", active="exact", href="/about"),
        dbc.NavLink(children="Datasets", href="/datasets"),
        dbc.NavLink(children="Outliers", href="/outliers"),
        dbc.NavLink(children="Inconsistencies", href="/inconsistencies"),
        dbc.NavLink(children="Missingness", href="/missingness"),
        dbc.NavLink(children="Feedback", href="/feedback", disabled=True),
    ],
)

# App layout
app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H4(
            "Feedback Loop System (FeeLoST)",
            style={"textAlign": "center"},
            className="bg-primary text-white p-2 mb-2 text-center",
        ),
        nav_menu,
        dbc.Container(id="page-content"),
        dash.page_container,
    ],
    # className="all",
)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
