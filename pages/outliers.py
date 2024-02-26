import dash
from dash import html, dcc, callback, Input, Output, dash_table

import dash_ag_grid as dag

import dash_bootstrap_components as dbc

import polars as pl

import plotly.io as pio
import plotly.express as px


pio.templates.default = "seaborn"

dash.register_page(__name__, name="FeeLoST", suppress_callback_exceptions=True)

hf_list_df = pl.read_csv("./data/input/hf_list_df.csv")

epi_outliers_df = (
    pl.read_csv("./data/input/epi_outliers_df.csv")
    .filter(pl.col("iqr").is_not_nan() | pl.col("zscore").is_not_nan() | pl.col("ttt").is_not_nan())
    .filter((pl.col("iqr") > 0) | (pl.col("zscore") > 0) | (pl.col("ttt") > 0))
    .join(hf_list_df, on=["hf_id", "hf_name"])
)


epi_outliers_agg = pl.read_csv("./data/input/epi_outliers_agg.csv")
epi_outliers_region_df = pl.read_csv("./data/input/epi_outliers_region_df.csv")
# epi_outliers_region_agg = pl.read_csv("./data/input/epi_outliers_region_agg.csv")
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

regions = epi_outliers_df["region"].unique().to_list()
zones = epi_outliers_df["zone"].unique().to_list()
woredas = epi_outliers_df["woreda"].unique().to_list()
levels = epi_outliers_df["level"].unique().to_list()
hf_types = epi_outliers_df["hf_type"].unique().to_list()
ownership = epi_outliers_df["ownership"].unique().to_list()

initial_vals = (
    epi_outliers_df.select(["region", "zone", "woreda", "level", "hf_type", "ownership"])
    .with_row_index(name="id")
    .filter(pl.col("id") == 0)
)

indicators = epi_outliers_df["indicator"].unique().to_list()

tab_outliers_region = html.Div(
    children=[
        html.Br(),
        dcc.Dropdown(
            id="tab-outliers-region-choice",
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
            [
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
                        ],
                    )
                ),
                html.Br(),
                dbc.Card(
                    dbc.CardBody(
                        children=[
                            # html.H6("Datasets"),
                            html.Br(),
                            html.Label("Indicator class"),
                            dcc.Dropdown(id="indicator-class", options=["Count"], value="Count"),
                            html.Br(),
                            html.Label("Outlier parameters"),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label("IQR: "),
                                        ],
                                        width=3,
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                id="iqr-param",
                                                options=[1.5, 3, 5],
                                                value=3,
                                            ),
                                        ],
                                        width=5,
                                    ),
                                ],
                                style={"padding-left": 20, "padding-top": 5},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label("Z-score: "),
                                        ],
                                        width=3,
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                id="iqr-param",
                                                options=[2, 3, 5],
                                                value=3,
                                            ),
                                        ],
                                        width=5,
                                    ),
                                ],
                                style={"padding-left": 20, "padding-top": 5},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label("TTT: "),
                                        ],
                                        width=3,
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                id="iqr-param",
                                                options=[0.95, 0.99],
                                                value=0.99,
                                            ),
                                        ],
                                        width=5,
                                    ),
                                ],
                                style={"padding-left": 20, "padding-top": 5},
                            ),
                        ],
                    )
                ),
            ],
            style={"padding": 10, "flex": 1},
        ),
        html.Div(
            children=[
                dbc.Card(
                    [
                        html.H3("Summary"),
                        html.P("The summary section provides"),
                        html.Ul(
                            [
                                html.Li(
                                    html.A(
                                        "Tables containing the number of outliers by several characteristics (region, level, facility type, ownership, and facility) and indicator, for each indicator."
                                    )
                                ),
                                html.Li(html.A("Graphs presenting the trend of the number of outliers. ")),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dcc.Tabs(
                                    id="tabs-outliers",
                                    value="tab-outliers-region",  # default selected tab
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
                                        dcc.Tab(label="Facility Type", value="tab-outliers-type"),
                                        dcc.Tab(label="Ownership", value="tab-outliers-ownership"),
                                        dcc.Tab(label="Health Facility", value="tab-outliers-hf"),
                                    ],
                                ),
                                html.Div(id="tabs-content-outliers"),
                            ],
                            # style={"padding": 10},
                        ),
                    ],
                    style={"padding": 10},
                ),
                html.Br(),
                html.Br(),
                dbc.Card(
                    [
                        html.H3("Health Facilities with Outliers"),
                        html.P("The table below shows the health facilities with outlier values."),
                        html.P(
                            "Users may choose the woreda of interest. In addition, users can filter the data on the table for more precise information."
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Region"),
                                        html.Div(
                                            dcc.Dropdown(
                                                id="outliers-region",
                                                options=regions,
                                                value=initial_vals["region"].item(),
                                            )
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Zone"),
                                        html.Div(
                                            dcc.Dropdown(
                                                id="outliers-zone",
                                                options=zones,
                                                value=initial_vals["zone"].item(),
                                            )
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Woreda"),
                                        html.Div(
                                            dcc.Dropdown(
                                                id="outliers-woreda",
                                                options=woredas,
                                                value=initial_vals["woreda"].item(),
                                            )
                                        ),
                                    ]
                                ),
                            ],
                            # style={"padding": 10},
                        ),
                        # dbc.Row(
                        #     [
                        #         dbc.Col(
                        #             [
                        #                 html.Label("Level"),
                        #                 html.Div(dcc.Dropdown(id="outliers-level", options=levels, value="")),
                        #             ]
                        #         ),
                        #         dbc.Col(
                        #             [
                        #                 html.Label("Type"),
                        #                 html.Div(dcc.Dropdown(id="outliers-type", options=hf_types, value="")),
                        #             ]
                        #         ),
                        #         dbc.Col(
                        #             [
                        #                 html.Label("Ownership"),
                        #                 html.Div(dcc.Dropdown(id="outliers-ownership", options=ownership, value="")),
                        #             ]
                        #         ),
                        #     ],
                        #     style={"padding": 10},
                        # ),
                        html.Br(),
                        dbc.Row(
                            [
                                html.Div(id="tab-outliers-df-content"),
                            ],
                            # style={"padding": 10},
                        ),
                    ],
                    style={"padding": 10},
                ),
            ],
            style={"padding": 10, "flex": 7},
        ),
    ],
    style={"display": "flex", "flexDirection": "row", "gap": "5px", "width": "100%"},
    # className="all",
)


# Backend Code
def month_to_numeric(month_name: str):

    # breakpoint()
    month = month_name.lower()

    if month == "january":
        return 1
    elif month == "february":
        return 2
    elif month == "march":
        return 3
    elif month == "april":
        return 4
    elif month == "may":
        return 5
    elif month == "june":
        return 6
    elif month == "july":
        return 7
    elif month == "august":
        return 8
    elif month == "september":
        return 9
    elif month == "october":
        return 10
    elif month == "november":
        return 11
    elif month == "december":
        return 12
    else:
        raise ValueError("The provided month does not exist!")


def compute_outliers_zones(df, region):

    df = df.select(["region", "zone"]).filter((pl.col("region").is_in(region)))
    zones = df["zone"].unique().to_list()

    return zones


def compute_outliers_woredas(df, region, zone):

    df = df.select(["region", "zone", "woreda"]).filter(
        (pl.col("region").is_in(region)) & (pl.col("zone").is_in(zone))
    )
    woredas = df["woreda"].unique().to_list()

    return woredas


@callback(
    Output(component_id="tab-outliers-df-content", component_property="children"),
    Output(component_id="outliers-zone", component_property="options"),
    Output(component_id="outliers-zone", component_property="value"),
    Output(component_id="outliers-woreda", component_property="options"),
    Output(component_id="outliers-woreda", component_property="value"),
    Input(component_id="datasets-list", component_property="value"),
    Input(component_id="outliers-region", component_property="value"),
    Input(component_id="outliers-zone", component_property="value"),
    Input(component_id="outliers-woreda", component_property="value"),
    # Input(component_id="outliers-level", component_property="value"),
    # Input(component_id="outliers-type", component_property="value"),
    # Input(component_id="outliers-ownership", component_property="value"),
)
def compute_outliers_df(dataset, region, zone, woreda):  # , level, type, ownership):

    match dataset:
        case "EPI":
            df = epi_outliers_df.select(
                [
                    "hf_name",
                    "region",
                    "zone",
                    "woreda",
                    "level",
                    "hf_type",
                    "ownership",
                    "period",
                    "indicator",
                    "value",
                    "iqr",
                    "zscore",
                    "ttt",
                ]
            )
        case _:
            raise ValueError("Selected dataset not found!")

    zones = compute_outliers_zones(df, [region])
    woredas = compute_outliers_woredas(df, [region], [zone])
    # breakpoint()

    df2 = df.filter(
        pl.col("region").is_in([region]), pl.col("zone").is_in([zone]), pl.col("woreda").is_in([woreda])
    )  # .filter(pl.col("level").is_in([level]) & pl.col("hf_type").is_in([type]) & pl.col("ownership").is_in([ownership]))

    return (
        [
            dag.AgGrid(
                rowData=df2.to_dicts(),
                columnDefs=[{"field": i} for i in df2.columns],
                defaultColDef={"filter": True, "sortable": True, "floatingFilter": True},
                persistence=True,
            )
        ],
        zones,
        zone,
        woredas,
        woreda,
    )  # df.to_dicts(), [{"field": i} for i in df.columns]


@callback(
    Output("tab-outliers-region-content", "children"),
    Input("tab-outliers-region-choice", "value"),
    Input("starting-month", "value"),
    Input("starting-year", "value"),
    Input("ending-month", "value"),
    Input("ending-year", "value"),
)
def outliers_tab_region(choice, start_month_name, start_year, end_month_name, end_year):

    start_month = month_to_numeric(start_month_name)
    end_month = month_to_numeric(end_month_name)

    # breakpoint()

    if start_year == end_year:
        epi_outliers_region_df2 = epi_outliers_region_df.filter(
            (
                (pl.col("month_code") >= start_month)
                & (pl.col("month_code") <= end_month)
                & (pl.col("year") == end_year)
            )
        )
    elif start_year < end_year:
        epi_outliers_region_df2 = epi_outliers_region_df.filter(
            ((pl.col("month_code") >= start_month) & (pl.col("year") == start_year))
            | ((pl.col("month_code") <= end_month) & (pl.col("year") == end_year))
            | ((pl.col("year") > start_year) & (pl.col("year") < end_year))
        )
    else:
        raise ValueError("Start date must be before than end date!")

    epi_outliers_region_agg2 = (
        epi_outliers_region_df2.group_by(["region", "indicator"])
        .agg(
            pl.col("iqr").drop_nans().sum().alias("iqr"),
            pl.col("zscore").drop_nans().sum().alias("zscore"),
            pl.col("ttt").drop_nans().sum().alias("ttt"),
        )
        .sort(by=["region", "indicator"])
    )

    match choice:
        case "Table":
            return html.Div(
                [
                    dash_table.DataTable(
                        id="outliers-region-tbl",
                        data=epi_outliers_region_agg2.to_dicts(),
                        columns=[
                            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                            for i in epi_outliers_region_agg2.columns
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
            df = epi_outliers_region_df2.select(["period", "iqr", "indicator"])
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
