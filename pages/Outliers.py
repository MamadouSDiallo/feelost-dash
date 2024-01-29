import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

import polars as pl

dash.register_page(__name__)


hf_list_df = pl.read_csv("./data/input/hf_list_df.csv")

epi_df = pl.read_csv("./data/input/epi_df.csv")


datasets_list = ["hf_list", "epi", "rmh"]
months = [
    "All",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


layout = html.Div(
    children=[
        html.Div(
            dbc.Card(
                dbc.CardBody(
                    children=[
                        # html.H6("Datasets"),
                        html.Br(),
                        html.Label("Dataset"),
                        dcc.Dropdown(id="datasets-list", options=datasets_list, value="hf_list"),
                        html.Br(),
                        html.Label("Number of rows"),
                        html.Div(dcc.Input(id="number-rows", type="number", value=15)),
                        html.Br(),
                        html.Br(),
                        html.Label("Time period (in years)"),
                        dcc.RangeSlider(
                            id="selected-years",
                            min=2012,
                            max=2020,
                            step=1,
                            value=[2014, 2014],
                            marks={i: str(i) for i in range(2012, 2021, 2)},
                        ),
                        html.Br(),
                        html.Label("Months of interest"),
                        dcc.Dropdown(id="selected-months", options=months, value="All", multi=True),
                    ],
                    # style={"padding": 10, "flex": 1},
                )
            ),
            style={"padding": 10, "flex": 1},
        ),
        html.Div(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Button(
                                        "Count",
                                        id="btn-count",
                                        n_clicks=0,
                                        className="bg-primary text-white p-2 mb-2 text-center",
                                        style={"flex": 1},
                                    ),
                                    # html.Br(),
                                    html.Button(
                                        "Percentage",
                                        id="btn-perc",
                                        n_clicks=0,
                                        className="bg-primary text-white p-2 mb-2 text-center",
                                        style={"flex": 1},
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "row",
                                    "gap": "150px",
                                    "align-items": "center",
                                    "padding": 30,
                                    "width": "100%",
                                    "height": "80px",
                                },
                            )
                        ],
                    )
                ),
                html.Br(),
                dbc.Card(
                    [
                        # html.H5("Metric Controls"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Interquartile Range (IQR)"),
                                        html.Div(dcc.Input(id="iqr-mult", type="number", value=1.5)),
                                        html.Button(
                                            "Select",
                                            id="btn-iqr",
                                            n_clicks=0,
                                            className="bg-primary text-white p-2 mb-2 text-center",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Standard Deviation (SD)"),
                                        html.Div(dcc.Input(id="sd-mult", type="number", value=2)),
                                        html.Button(
                                            "Select",
                                            id="btn-sd",
                                            n_clicks=0,
                                            className="bg-primary text-white p-2 mb-2 text-center",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Thompson Tau Test (TTT)"),
                                        html.Div(dcc.Input(id="ttt-perc", type="number", min=1, max=100, value=95)),
                                        html.Button(
                                            "Select",
                                            id="btn-ttt",
                                            n_clicks=0,
                                            className="bg-primary text-white p-2 mb-2 text-center",
                                        ),
                                    ]
                                ),
                            ],
                            style={
                                "padding": 10,
                                # "align-items": "center",
                            },
                        ),
                    ],
                ),
                html.Br(),
                dbc.Card(html.H5("Summary", style={"padding": 10})),
                html.Br(),
                dbc.Card(html.H5("Health Facilities with Outliers", style={"padding": 10})),
            ],
            style={"padding": 10, "flex": 3},
        ),
    ],
    style={"display": "flex", "flexDirection": "row", "gap": "5px", "width": "100%"},
    className="all",
)
