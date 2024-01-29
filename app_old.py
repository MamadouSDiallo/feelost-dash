# Import packages
from dash import Dash, html, dcc
import dash_auth
import dash_bootstrap_components as dbc

# from script.datasets import datasets_fe, datasets_be

from env.secrets import VALID_USERNAME_PASSWORD_PAIRS


# Initialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)


nav_menu = dbc.Nav(
    id="nav-bar",
    children=[
        dbc.NavLink(children="About FeeloST", active="exact", href="/about"),
        dbc.NavLink(children="Datasets", href="/datasets"),
        dbc.NavLink(children="Outliers", href="/outliers"),
        dbc.NavLink(children="Inconsistencies", href="/inconsistencies"),
        dbc.NavLink(children="Missingness", href="/missingness"),
        dbc.NavLink(children="Feedback", href="feedback"),
        dbc.NavLink(children="Disabled", disabled=True, href="/"),
    ],
)


about = html.Div(html.H6("About FeeLoST"), id="about")

outliers = html.Div(html.H6("Outliers"), id="outliers")

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
        # html.Div(children=[about, outliers, datasets], style={"display": "block"}),
    ]
    # children=[
    #     html.H1("Feedback Loop System (FeeLoST)", style={"textAlign": "center"}),
    #     dcc.Tabs(
    #         id="tabs-feelost",
    #         value="tab-value",
    #         children=[
    #             dcc.Tab(label="Tab One", value="tab-1-example-graph"),
    #             dcc.Tab(label="Tab Two", value="tab-2-example-graph"),
    #         ],
    #     ),
    # ]
)


# Add controls to build the interaction
# @app.callback(
#     Output(component_id="page-content", component_property="children"),
#     Input(component_id="url", component_property="pathname"),
# )
# def render_page(pathname):
#     if pathname in ["/", "/about"]:
#         return about
#     elif pathname in ["/datasets"]:
#         return datasets_fe
#     elif pathname in ["/outliers"]:
#         return outliers
#     else:
#         return html.P("This is else")


# def dataset_table():
#     return datasets_be()


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
