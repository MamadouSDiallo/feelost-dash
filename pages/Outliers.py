import dash
from dash import html, dcc, callback, Input, Output, dash_table

import dash_bootstrap_components as dbc

import numpy as np
import polars as pl


from script.outlier_metrics import outlier_iqr

dash.register_page(__name__)


datasets_list = ["epi"]
years = [2013, 2014, 2015]
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
quarters = ["All", "Q1", "Q2", "Q3", "Q4"]

# Frontend
layout = html.Div(
    children=[
        html.Div(
            dbc.Card(
                dbc.CardBody(
                    children=[
                        # html.H6("Datasets"),
                        html.Br(),
                        html.Label("Dataset"),
                        dcc.Dropdown(id="datasets-list", options=datasets_list, value="epi"),
                        html.Br(),
                        html.Label("Number of rows"),
                        html.Div(dcc.Input(id="number-rows", type="number", value=15)),
                        html.Br(),
                        html.Br(),
                        html.Label("Starting period"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        # html.Label("Year: "),
                                        dcc.Dropdown(
                                            id="starting-year",
                                            options=years,
                                            value=2013,
                                        ),
                                    ],
                                    width=5,
                                ),
                                dbc.Col(
                                    [
                                        # html.Label("Month: "),
                                        dcc.Dropdown(
                                            id="starting-month",
                                            options=months,
                                            value="January",
                                        ),
                                    ],
                                    width=7,
                                ),
                            ],
                            # style={"display": "flex", "flexDirection": "row"},
                        ),
                        html.Br(),
                        html.Label("Ending period"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        # html.Label("Year: "),
                                        dcc.Dropdown(
                                            id="ending-year",
                                            options=years,
                                            value=2013,
                                        ),
                                    ],
                                    width=5,
                                ),
                                dbc.Col(
                                    [
                                        # html.Label("Month: "),
                                        dcc.Dropdown(
                                            id="ending-month",
                                            options=months,
                                            value="January",
                                        ),
                                    ],
                                    width=7,
                                ),
                            ]
                        ),
                        # html.Label("Time period (in years)"),
                        # dcc.RangeSlider(
                        #     id="selected-years",
                        #     min=2012,
                        #     max=2020,
                        #     step=1,
                        #     value=[2014, 2014],
                        #     marks={i: str(i) for i in range(2012, 2021, 2)},
                        # ),
                        # html.Br(),
                        # html.Label("Quarters of interest"),
                        # dcc.Dropdown(id="selected-quarters", options=quarters, value="All", multi=True),
                        # html.Br(),
                        # html.Label("Months of interest"),
                        # dcc.Dropdown(id="selected-months", options=months, value="All", multi=True),
                    ],
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
                                        # html.Button(
                                        #     "Select",
                                        #     id="btn-iqr",
                                        #     n_clicks=0,
                                        #     className="bg-primary text-white p-2 mb-2 text-center",
                                        # ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Standard Deviation (SD)"),
                                        html.Div(dcc.Input(id="sd-mult", type="number", value=2)),
                                        # html.Button(
                                        #     "Select",
                                        #     id="btn-sd",
                                        #     n_clicks=0,
                                        #     className="bg-primary text-white p-2 mb-2 text-center",
                                        # ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Thompson Tau Test (TTT)"),
                                        html.Div(dcc.Input(id="ttt-perc", type="number", min=1, max=100, value=95)),
                                        # html.Button(
                                        #     "Select",
                                        #     id="btn-ttt",
                                        #     n_clicks=0,
                                        #     className="bg-primary text-white p-2 mb-2 text-center",
                                        # ),
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
                dbc.Card(
                    [
                        html.H5("Summary", style={"padding": 10}),
                        dbc.Row(
                            [
                                dash_table.DataTable(id="outliers-dataset"),
                            ]
                        ),
                    ]
                ),
                html.Br(),
                dbc.Card(
                    html.H5("Health Facilities with Outliers", style={"padding": 10}),
                ),
            ],
            style={"padding": 10, "flex": 3},
        ),
    ],
    style={"display": "flex", "flexDirection": "row", "gap": "5px", "width": "100%"},
    className="all",
)


# Backend


@callback(
    Output(component_id="outliers-dataset", component_property="data"),
    Input(component_id="datasets-list", component_property="value"),
    Input(component_id="starting-year", component_property="value"),
    Input(component_id="starting-month", component_property="value"),
    Input(component_id="ending-year", component_property="value"),
    Input(component_id="ending-month", component_property="value"),
    Input(component_id="iqr-mult", component_property="value"),
    Input(component_id="sd-mult", component_property="value"),
    Input(component_id="ttt-perc", component_property="value"),
)
def compute_outliers(dataset, start_year, start_month, end_year, end_month, iqr_fct, sd_fct, ttt_perc):
    begin = {"month": start_month, "year": start_year}
    end = {"month": end_month, "year": end_year}
    factor = {"iqr": iqr_fct, "sd": sd_fct, "ttt": ttt_perc}

    # before_months = []
    # month1 = "January"
    # while month1 != begin["month"]:
    #     before_months.append(month1)

    # after_months = []
    # month2 = months.copy()
    # while month2 != begin["month"]:
    #     after_months.remove(month2)
    # after_months.remove(month2)

    match dataset:
        case "epi":
            outliers_df = epi_outliers(begin, end, factor)
        case _:
            raise ValueError("Selected dataset not found!")

    return outliers_df.to_dicts()


def epi_outliers(begin, end, factor):
    epi_inds = ["bcg", "ipv", "penta1", "penta3", "mcv1", "rota2", "full_vacc"]
    epi_inds.append("hf_id")
    # regions = epi_ind.select("region").unique().to_series().sort().to_list()
    epi_df = pl.read_csv("./data/input/epi_ind.csv").select(epi_inds)
    hf_list = epi_df.select("hf_id").unique().to_series()
    nb_cols = len(epi_df.columns) - 1
    hf_ids = np.repeat(hf_list, repeats=nb_cols)
    col_names = np.array([])

    epi_iqr = np.array([])
    for hf in hf_list:
        epi_hf = epi_df.filter(pl.col("hf_id") == hf).drop("hf_id")
        col_names = np.append(col_names, epi_hf.columns)
        for col in epi_hf.columns:
            # breakpoint()
            epi_iqr = np.append(epi_iqr, outlier_iqr(epi_hf[col].to_numpy(), factor=factor["iqr"]).sum())
            # outlier_sd(epi_hf[col].to_numpy(), factor=factor["sd"]).sum()
            # outlier_ttt(epi_hf[col].to_numpy(), factor=factor["ttt"]).sum()

    breakpoint()
    epi_hfs = pl.DataFrame({"hf_id": hf_ids, "iqr": epi_iqr})
    return epi_hfs
