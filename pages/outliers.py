import dash
from dash import html, dcc, callback, Input, Output, dash_table

import dash_bootstrap_components as dbc

import polars as pl

import plotly.io as pio
import plotly.express as px

pio.templates.default = "seaborn"

dash.register_page(__name__, name="FeeLoST")

hf_list_df = pl.read_csv("./data/input/hf_list_df.csv")
epi_outliers_df = pl.read_csv("./data/input/epi_outliers_df.csv")
epi_outliers_agg = pl.read_csv("./data/input/epi_outliers_agg.csv")
epi_outliers_region_df = pl.read_csv("./data/input/epi_outliers_region_df.csv")
epi_outliers_region_agg = pl.read_csv("./data/input/epi_outliers_region_agg.csv")
epi_outliers_level_df = pl.read_csv("./data/input/epi_outliers_level_df.csv")
epi_outliers_level_agg = pl.read_csv("./data/input/epi_outliers_level_agg.csv")


datasets_list = ["EPI"]
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

regions = hf_list_df["region"].unique().to_list()
zones = hf_list_df["zone"].unique().to_list()
woredas = hf_list_df["woreda"].unique().to_list()
levels = hf_list_df["level"].unique().to_list()
hf_types = hf_list_df["hf_type"].unique().to_list()
ownership = hf_list_df["ownership"].unique().to_list()

indicators = epi_outliers_df["indicator"].unique().to_list()

tab_outliers_region = html.Div(
    children=[
        html.Br(),
        dcc.Dropdown(
            id="outliers-region-content-choice",
            options=["Table", "Trend"],
            value="Table",
            style={"width": "50%"},
        ),
        html.Br(),
        html.Div(id="tab-outliers-region-content"),
    ],
    # style={"padding": 10},
)

tab_outliers_level = html.Div(
    children=[
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="outliers-level-content-choice",
                        options=["Table", "Trend"],
                        value="Table",
                        # style={"width": "50%"},
                    ),
                    width=5,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="outliers-level-content-choice2",
                        options=indicators,
                        value="bcg",
                        # style={"width": "50%"},
                    ),
                    width=5,
                ),
            ],
            style={"width": "50%"},
        ),
        html.Br(),
        html.Div(id="tab-outliers-level-content"),
    ],
    # style={"padding": 10},
)


# Frontend
layout = html.Div(
    children=[
        html.Div(
            dbc.Card(
                dbc.CardBody(
                    children=[
                        # html.H6("Datasets"),
                        html.Br(),
                        html.Label("Department"),
                        dcc.Dropdown(id="datasets-list", options=datasets_list, value="EPI"),
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
                                            value="November",
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
                                            value=2015,
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
                                            value="October",
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
                                        html.Div(dcc.Input(id="iqr-mult", type="number", value=3)),
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
                                        html.Div(dcc.Input(id="sd-mult", type="number", value=3)),
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
                                        html.Div(dcc.Input(id="ttt-perc", type="number", min=1, max=100, value=99)),
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
                                dcc.Tabs(
                                    id="tabs-outliers",
                                    value="tab-outliers-region",
                                    children=[
                                        dcc.Tab(
                                            label="Region",
                                            value="tab-outliers-region",
                                            children=tab_outliers_region,
                                        ),
                                        dcc.Tab(
                                            label="Administrative Level",
                                            value="tab-outliers-level",
                                            children=tab_outliers_level,
                                        ),
                                        dcc.Tab(label="Health Facility Type", value="tab-outliers-type"),
                                        dcc.Tab(label="Ownership", value="tab-outliers-ownership"),
                                        dcc.Tab(label="Health Facility", value="tab-outliers-hf"),
                                    ],
                                ),
                                html.Div(id="tabs-content-outliers"),
                            ],
                            style={"padding": 10},
                        ),
                    ]
                ),
                html.Br(),
                html.Br(),
                dbc.Card(
                    [
                        html.H5("Health Facilities with Outliers", style={"padding": 10}),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Region"),
                                        html.Div(
                                            dcc.Dropdown(id="outliers-region", options=regions, value=regions[0])
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Zone"),
                                        html.Div(dcc.Dropdown(id="outliers-zone", options=zones, value="")),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Woreda"),
                                        html.Div(dcc.Dropdown(id="outliers-woreda", options=woredas, value="")),
                                    ]
                                ),
                            ],
                            style={"padding": 10},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Level"),
                                        html.Div(dcc.Dropdown(id="outliers-levels", options=levels, value="")),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Type"),
                                        html.Div(dcc.Dropdown(id="outliers-types", options=hf_types, value="")),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Ownership"),
                                        html.Div(dcc.Dropdown(id="outliers-ownership", options=ownership, value="")),
                                    ]
                                ),
                            ],
                            style={"padding": 10},
                        ),
                        dbc.Row(
                            [
                                dash_table.DataTable(
                                    id="outliers-df",
                                    editable=False,
                                    filter_action="native",
                                    sort_action="native",
                                    sort_mode="single",
                                    column_selectable="multi",
                                    page_action="native",
                                    page_current=0,
                                    page_size=15,
                                    style_table={
                                        "overflowX": "auto",
                                        "maxWidth": "100%",
                                        "marginLeft": "auto",
                                        "marginRight": "auto",
                                    },
                                ),
                            ],
                            style={"padding": 10},
                        ),
                    ]
                ),
            ],
            style={"padding": 10, "flex": 3},
        ),
    ],
    style={"display": "flex", "flexDirection": "row", "gap": "5px", "width": "100%"},
    # className="all",
)


# Backend


# @callback(
#     Output(component_id="outliers-agg", component_property="data"),
#     Output(component_id="outliers-agg", component_property="columns"),
#     Input(component_id="datasets-list", component_property="value"),
#     Input(component_id="starting-year", component_property="value"),
#     Input(component_id="starting-month", component_property="value"),
#     Input(component_id="ending-year", component_property="value"),
#     Input(component_id="ending-month", component_property="value"),
#     Input(component_id="iqr-mult", component_property="value"),
#     Input(component_id="sd-mult", component_property="value"),
#     Input(component_id="ttt-perc", component_property="value"),
# )
# def compute_outliers_agg(dataset, start_year, start_month, end_year, end_month, iqr_fct, sd_fct, ttt_perc):
#     begin = {"month": start_month, "year": start_year}
#     end = {"month": end_month, "year": end_year}
#     factor = {"iqr": iqr_fct, "sd": sd_fct, "ttt": (100 - (100 - ttt_perc) / 2) / 100}

#     # before_months = []
#     # month1 = "January"
#     # while month1 != begin["month"]:
#     #     before_months.append(month1)

#     # after_months = []
#     # month2 = months.copy()
#     # while month2 != begin["month"]:
#     #     after_months.remove(month2)
#     # after_months.remove(month2)

#     match dataset:
#         case "epi":
#             outliers_agg = epi_outliers_agg(begin, end, factor)
#         case _:
#             raise ValueError("Selected dataset not found!")

#     return outliers_agg.to_dicts(), [
#         {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
#         for i in outliers_agg.columns
#         if i != "hf_id"
#     ]

# def epi_outliers_agg(begin, end, factor):
#     epi_outliers_agg = pl.read_csv("./data/input/epi_outliers_agg.csv")

#     return epi_outliers_agg


@callback(
    Output(component_id="outliers-df", component_property="data"),
    Output(component_id="outliers-df", component_property="columns"),
    Input(component_id="datasets-list", component_property="value"),
    Input(component_id="starting-year", component_property="value"),
    Input(component_id="starting-month", component_property="value"),
    Input(component_id="ending-year", component_property="value"),
    Input(component_id="ending-month", component_property="value"),
    Input(component_id="iqr-mult", component_property="value"),
    Input(component_id="sd-mult", component_property="value"),
    Input(component_id="ttt-perc", component_property="value"),
)
def compute_outliers_df(dataset, start_year, start_month, end_year, end_month, iqr_fct, sd_fct, ttt_perc):
    begin = {"month": start_month, "year": start_year}
    end = {"month": end_month, "year": end_year}
    factor = {"iqr": iqr_fct, "sd": sd_fct, "ttt": (100 - (100 - ttt_perc) / 2) / 100}

    match dataset:
        case "EPI":
            outliers_df = epi_outliers_df(begin, end, factor)
        case _:
            raise ValueError("Selected dataset not found!")

    return outliers_df.to_dicts(), [
        {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
        for i in outliers_df.columns
        if i != "hf_id"
    ]


def epi_outliers_df(begin, end, factor):
    epi_outliers_df = pl.read_csv("./data/input/epi_outliers_df.csv")

    return epi_outliers_df


@callback(Output("tab-outliers-region-content", "children"), Input("outliers-region-content-choice", "value"))
def outliers_tab_region(choice):
    match choice:
        case "Table":
            return html.Div(
                [
                    dash_table.DataTable(
                        id="outliers-region-tbl",
                        data=epi_outliers_region_agg.to_dicts(),
                        columns=[
                            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                            for i in epi_outliers_region_agg.columns
                        ],
                        editable=False,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="single",
                        column_selectable="multi",
                        page_action="native",
                        page_current=0,
                        page_size=15,
                        style_table={
                            "overflowX": "auto",
                            "maxWidth": "100%",
                            "marginLeft": "auto",
                            "marginRight": "auto",
                        },
                    ),
                ]
            )
        case "Trend":
            # y_min = epi_outliers_region_df["iqr"].min()
            # y_max = epi_outliers_region_df["iqr"].max()
            df = epi_outliers_region_df.select(["period", "iqr", "indicator"])
            fig = px.scatter(
                data_frame=df,
                x="period",
                y="iqr",
                # range_y=[0.9 * y_min, 1.1 * y_max],
                color="indicator",
                # symbol=incons_flag,
                # size=nb_infants,
                title="Number of Outliers by Vaccine",
            )
            fig.update_xaxes(tickangle=60, title_text=None)
            fig.update_yaxes(title_text=None)
            fig.update_layout(legend_title_text="Vaccine")
            return html.Div([dcc.Graph(figure=fig)])
        case _:
            pass


@callback(
    Output("tab-outliers-level-content", "children"),
    Input("outliers-level-content-choice", "value"),
    Input("outliers-level-content-choice2", "value"),
)
def outliers_tab_level(choice, vaccine):
    match choice:
        case "Table":
            return html.Div(
                [
                    dash_table.DataTable(
                        id="outliers-level-tbl",
                        data=epi_outliers_level_agg.to_dicts(),
                        columns=[
                            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                            for i in epi_outliers_level_agg.columns
                        ],
                        editable=False,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="single",
                        column_selectable="multi",
                        page_action="native",
                        page_current=0,
                        page_size=15,
                        style_table={
                            "overflowX": "auto",
                            "maxWidth": "100%",
                            "marginLeft": "auto",
                            "marginRight": "auto",
                        },
                    ),
                ]
            )
        case "Trend":
            df = (
                epi_outliers_level_df.filter(pl.col("indicator") == vaccine)
                .select(["period", "iqr", "level"])
                .cast({"level": pl.Utf8})
            )
            fig = px.scatter(
                data_frame=df,
                x="period",
                y="iqr",
                # range_y=[0, 1.1 * y_max],
                color="level",
                # symbol=incons_flag,
                # size=nb_infants,
                title="Number of Outliers by Vaccine",
            )
            fig.update_xaxes(tickangle=60, title_text=None)
            fig.update_yaxes(title_text=None)
            fig.update_layout(legend_title_text="Level")
            return html.Div([dcc.Graph(figure=fig)])
        case _:
            pass


# @callback()
# def outliers_tab_hf():
#     return (
#         dash_table.DataTable(
#             id="outliers-agg",
#             editable=False,
#             filter_action="native",
#             sort_action="native",
#             sort_mode="single",
#             column_selectable="multi",
#             page_action="native",
#             page_current=0,
#             page_size=15,
#             style_table={
#                 "overflowX": "auto",
#                 "maxWidth": "100%",
#                 "marginLeft": "auto",
#                 "marginRight": "auto",
#             },
#         ),
#     )
