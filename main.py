# Import packages
import dash
<<<<<<< HEAD:main.py
from dash import Dash, html, dcc, Input, Output, callback
=======
from dash import Dash, html, dcc

# import dash_auth
>>>>>>> 85c5fee9d5e878fc867614372f0489f4298e9238:app.py
import dash_bootstrap_components as dbc

# import dash_enterprise_auth as auth

<<<<<<< HEAD:main.py
# import dash_auth
# from env.secrets import VALID_USERNAME_PASSWORD_PAIRS
=======
# from script.datasets import datasets_fe, datasets_be
>>>>>>> 85c5fee9d5e878fc867614372f0489f4298e9238:app.py


# Initialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
<<<<<<< HEAD:main.py

# auth = dash_auth.BasicAuth(server, VALID_USERNAME_PASSWORD_PAIRS)

=======

# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
>>>>>>> 85c5fee9d5e878fc867614372f0489f4298e9238:app.py

app.title = "FeeLoST"

nav_menu = dbc.Nav(
    id="nav-bar",
    children=[
        dbc.NavLink(children="About FeeLoST", href="/about"),
        dbc.NavLink(children="Datasets", href="/datasets"),
        dbc.NavLink(children="Outliers", href="/outliers"),
        dbc.NavLink(children="Inconsistencies", href="/inconsistencies", disabled=True),
        dbc.NavLink(children="Missingness", href="/missingness", disabled=True),
        dbc.NavLink(children="Feedback", href="/feedback"),
    ],
)

# App layout
app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H4(
            "Feedback Loop System (FeeLoST)",
<<<<<<< HEAD:main.py
            id='header-title',
            style={"textAlign": "center"},
            className="bg-primary text-white p-2 mb-2 text-center",
        ),
        # html.Div(auth.create_logout_button(), className='two columns', style={'marginTop': 30}),
=======
            id="header-title",
            style={"textAlign": "center"},
            className="bg-primary text-white p-2 mb-2 text-center",
        ),
        # html.Div(auth.create_logout_button(), className="two columns", style={"marginTop": 30}),
>>>>>>> 85c5fee9d5e878fc867614372f0489f4298e9238:app.py
        # html.Div(id="auth-input", style={"display": "none"}),
        nav_menu,
        dbc.Container(id="page-content"),
        dash.page_container,
    ],
    style={"margin-left": "7px", "margin-right": "7px", "margin-top": "7px"},
    # className="all",
)

<<<<<<< HEAD:main.py
# @callback(Output("header-title", "children"), Input("url", "pathname"))
=======

# @callback(Output("header-title", "children"), Input("auth-input", "children"))
>>>>>>> 85c5fee9d5e878fc867614372f0489f4298e9238:app.py
# def update_title(_):

#     # print user data to the logs
#     print(auth.get_user_data())

#     # update header with username
#     return "Hello {}".format(auth.get_username())
<<<<<<< HEAD:main.py

# Run the app
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=Truey, host="0.0.0.0", port="8080", use_reloader=False)
=======


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host="0.0.0.0", port="8080", use_reloader=False)
>>>>>>> 85c5fee9d5e878fc867614372f0489f4298e9238:app.py
