# Import packages
import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

# import dash_enterprise_auth as auth

# import dash_auth
# from env.secrets import VALID_USERNAME_PASSWORD_PAIRS


# Initialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# auth = dash_auth.BasicAuth(server, VALID_USERNAME_PASSWORD_PAIRS)


app.title = "FeeLoST"

nav_menu = dbc.Nav(
    id="nav-bar",
    children=[
        dbc.NavLink(children="About FeeLoST", href="/"),
        dbc.NavLink(children="Datasets", href="/datasets"),
        dbc.NavLink(children="Outliers", href="/outliers"),
        dbc.NavLink(children="Inconsistencies", href="/inconsistencies", disabled=True),
        dbc.NavLink(children="Missingness", href="/missingness", disabled=True),
        dbc.NavLink(children="Feedback", href="/feedback", disabled=True),
    ],
)

# App layout
app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H4(
            "Feedback Loop System (FeeLoST)",
            id='header-title',
            style={"textAlign": "center"},
            className="bg-primary text-white p-2 mb-2 text-center",
        ),
        # html.Div(auth.create_logout_button(), className='two columns', style={'marginTop': 30}),
        # html.Div(id="auth-input", style={"display": "none"}),
        nav_menu,
        dbc.Container(id="page-content"),
        dash.page_container,
    ],
    style={"margin-left": "7px", "margin-right": "7px", "margin-top": "7px"},
    # className="all",
)

# @callback(Output("header-title", "children"), Input("url", "pathname"))
# def update_title(_):

#     # print user data to the logs
#     print(auth.get_user_data())

#     # update header with username
#     return "Hello {}".format(auth.get_username())

# Run the app
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=Truey, host="0.0.0.0", port="8080", use_reloader=False)
