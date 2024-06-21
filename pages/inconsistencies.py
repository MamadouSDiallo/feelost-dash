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

epi_inconsis_df = (
    pl.read_csv("./data/input/epi_inconsis_df.csv")
    .filter(
        pl.col("bcg").is_not_null()
        | pl.col("ipv").is_not_null()
        | pl.col("penta1").is_not_null()
        | pl.col("penta3").is_not_null()
        | pl.col("penta_all_ages").is_not_null()
        | pl.col("mcv1").is_not_null()
        | pl.col("mcv_all_ages").is_not_null()
        | pl.col("rota2").is_not_null()
        | pl.col("full_vacc").is_not_null()
    )
    .filter(
        (pl.col("bcg") > 0)
        | (pl.col("ipv") > 0)
        | (pl.col("penta1") > 0)
        | (pl.col("penta3") > 0)
        | (pl.col("penta_all_ages") > 0)
        | (pl.col("mcv1") > 0)
        | (pl.col("mcv_all_ages") > 0)
        | (pl.col("rota2") > 0)
        | (pl.col("full_vacc") > 0)
    )
    .join(hf_list_df, on=["hf_id", "hf_name"])
)


epi_inconsis_region_df = pl.read_csv("./data/input/epi_inconsis_region_df.csv")
epi_inconsis_level_df = pl.read_csv("./data/input/epi_inconsis_level_df.csv")


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

regions = epi_inconsis_df["region"].unique().to_list()
zones = epi_inconsis_df["zone"].unique().to_list()
woredas = epi_inconsis_df["woreda"].unique().to_list()
levels = epi_inconsis_df["level"].unique().to_list()
hf_types = epi_inconsis_df["hf_type"].unique().to_list()
ownership = epi_inconsis_df["ownership"].unique().to_list()

initial_vals = (
    epi_inconsis_df.select(["region", "zone", "woreda", "level", "hf_type", "ownership"])
    .with_row_index(name="id")
    .filter(pl.col("id") == 0)
)


tab_inconsis_region = html.Div(
    children=[
        html.Br(),
        dcc.Dropdown(
            id="tab-inconsis-region-choice",
            options=["Table", "Trend"],
            value="Table",
            style={"width": "50%"},
        ),
        html.Br(),
        html.Div(id="tab-inconsis-region-content"),
    ],
    # style={"padding": 10},
)


tab_inconsis_level = html.Div(
    children=[
        html.Br(),
        dcc.Dropdown(
            id="tab-inconsis-level-choice",
            options=["Table", "Trend"],
            value="Table",
            style={"width": "50%"},
        ),
        html.Br(),
        html.Div(id="tab-inconsis-level-content"),
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
            ],
            style={"padding": 10, "flex": 2},
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
                                        "Tables containing the number of inconsistent data points by several characteristics (region, level, facility type, ownership, and facility) for each indicator."
                                    )
                                ),
                                html.Li(
                                    html.A("Graphs presenting the trend of the number of inconsistent data points. ")
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dcc.Tabs(
                                    id="tabs-inconsis",
                                    value="tab-inconsis-region",  # default selected tab
                                    children=[
                                        dcc.Tab(
                                            label="Region",
                                            value="tab-inconsis-region",
                                            children=tab_inconsis_region,
                                        ),
                                        dcc.Tab(
                                            label="Administrative Level",
                                            value="tab-inconsis-level",
                                            children=tab_inconsis_level,
                                        ),
                                        dcc.Tab(label="Facility Type", value="tab-inconsis-type"),
                                        dcc.Tab(label="Ownership", value="tab-inconsis-ownership"),
                                        dcc.Tab(label="Health Facility", value="tab-inconsis-hf"),
                                    ],
                                ),
                                html.Div(id="tabs-content-inconsis"),
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
                        html.H3("Health Facilities with Inconsistent Data Points"),
                        html.P("The table below shows the health facilities with inconsistent data points."),
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
                                                id="inconsis-region",
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
                                                id="inconsis-zone",
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
                                                id="inconsis-woreda",
                                                options=woredas,
                                                value=initial_vals["woreda"].item(),
                                            )
                                        ),
                                    ]
                                ),
                            ],
                            # style={"padding": 10},
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                html.Div(id="tab-inconsis-df-content"),
                            ],
                            # style={"padding": 10},
                        ),
                    ],
                    style={"padding": 10},
                ),
            ],
            style={"padding": 10, "flex": 6},
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


def compute_inconsis_zones(df, region):

    df = df.select(["region", "zone"]).filter((pl.col("region").is_in(region)))
    zones = df["zone"].unique().to_list()

    return zones


def compute_inconsis_woredas(df, region, zone):

    df = df.select(["region", "zone", "woreda"]).filter(
        (pl.col("region").is_in(region)) & (pl.col("zone").is_in(zone))
    )
    woredas = df["woreda"].unique().to_list()

    return woredas


@callback(
    Output("tab-inconsis-region-content", "children"),
    Input("tab-inconsis-region-choice", "value"),
    Input("starting-month", "value"),
    Input("starting-year", "value"),
    Input("ending-month", "value"),
    Input("ending-year", "value"),
)
def inconsis_tab_region(choice, start_month_name, start_year, end_month_name, end_year):

    start_month = month_to_numeric(start_month_name)
    end_month = month_to_numeric(end_month_name)

    # breakpoint()

    if start_year == end_year:
        epi_inconsis_region_df2 = epi_inconsis_region_df.filter(
            (
                (pl.col("month_code") >= start_month)
                & (pl.col("month_code") <= end_month)
                & (pl.col("year") == end_year)
            )
        )
    elif start_year < end_year:
        epi_inconsis_region_df2 = epi_inconsis_region_df.filter(
            ((pl.col("month_code") >= start_month) & (pl.col("year") == start_year))
            | ((pl.col("month_code") <= end_month) & (pl.col("year") == end_year))
            | ((pl.col("year") > start_year) & (pl.col("year") < end_year))
        )
    else:
        raise ValueError("Start date must be before than end date!")

    epi_inconsis_region_agg2 = (
        epi_inconsis_region_df2.group_by(["region"])
        .agg(
            pl.col("bcg").drop_nans().sum().alias("bcg"),
            pl.col("ipv").drop_nans().sum().alias("ipv"),
            pl.col("penta1").drop_nans().sum().alias("penta1"),
            pl.col("penta3").drop_nans().sum().alias("penta3"),
            pl.col("penta_all_ages").drop_nans().sum().alias("penta_all_ages"),
            pl.col("mcv1").drop_nans().sum().alias("mcv1"),
            pl.col("mcv_all_ages").drop_nans().sum().alias("mcv_all_ages"),
            pl.col("rota2").drop_nans().sum().alias("rota1"),
            pl.col("full_vacc").drop_nans().sum().alias("full_vacc"),
        )
        .sort(by=["region"])
    )

    match choice:
        case "Table":
            return html.Div(
                [
                    dash_table.DataTable(
                        id="inconsis-region-tbl",
                        data=epi_inconsis_region_agg2.to_dicts(),
                        columns=[
                            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                            for i in epi_inconsis_region_agg2.columns
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
            df = epi_inconsis_region_df2.select(["period", "bcg"])
            fig = px.scatter(
                data_frame=df,
                x="period",
                y="bcg",
                # color="indicator",
                title="Number of inconsistent data points by Vaccine",
            )
            fig.update_xaxes(tickangle=60, title_text=None)
            fig.update_yaxes(title_text=None)
            fig.update_layout(legend_title_text="Vaccine")
            return html.Div([dcc.Graph(figure=fig)])
        case _:
            pass


@callback(
    Output("tab-inconsis-level-content", "children"),
    Input("tab-inconsis-level-choice", "value"),
    Input("starting-month", "value"),
    Input("starting-year", "value"),
    Input("ending-month", "value"),
    Input("ending-year", "value"),
)
def inconsis_tab_level(choice, start_month_name, start_year, end_month_name, end_year):

    start_month = month_to_numeric(start_month_name)
    end_month = month_to_numeric(end_month_name)

    # breakpoint()

    if start_year == end_year:
        epi_inconsis_level_df2 = epi_inconsis_level_df.filter(
            (
                (pl.col("month_code") >= start_month)
                & (pl.col("month_code") <= end_month)
                & (pl.col("year") == end_year)
            )
        )
    elif start_year < end_year:
        epi_inconsis_level_df2 = epi_inconsis_level_df.filter(
            ((pl.col("month_code") >= start_month) & (pl.col("year") == start_year))
            | ((pl.col("month_code") <= end_month) & (pl.col("year") == end_year))
            | ((pl.col("year") > start_year) & (pl.col("year") < end_year))
        )
    else:
        raise ValueError("Start date must be before than end date!")

    epi_inconsis_level_agg2 = (
        epi_inconsis_level_df2.group_by(["level"])
        .agg(
            pl.col("bcg").drop_nans().sum().alias("bcg"),
            pl.col("ipv").drop_nans().sum().alias("ipv"),
            pl.col("penta1").drop_nans().sum().alias("penta1"),
            pl.col("penta3").drop_nans().sum().alias("penta3"),
            pl.col("penta_all_ages").drop_nans().sum().alias("penta_all_ages"),
            pl.col("mcv1").drop_nans().sum().alias("mcv1"),
            pl.col("mcv_all_ages").drop_nans().sum().alias("mcv_all_ages"),
            pl.col("rota2").drop_nans().sum().alias("rota1"),
            pl.col("full_vacc").drop_nans().sum().alias("full_vacc"),
        )
        .sort(by=["level"])
    )

    match choice:
        case "Table":
            return html.Div(
                [
                    dash_table.DataTable(
                        id="inconsis-level-tbl",
                        data=epi_inconsis_level_agg2.to_dicts(),
                        columns=[
                            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                            for i in epi_inconsis_level_agg2.columns
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
            df = epi_inconsis_level_df2.select(["period", "bcg"])
            fig = px.scatter(
                data_frame=df,
                x="period",
                y="bcg",
                # color="indicator",
                title="Number of inconsis by Vaccine",
            )
            fig.update_xaxes(tickangle=60, title_text=None)
            fig.update_yaxes(title_text=None)
            fig.update_layout(legend_title_text="Vaccine")
            return html.Div([dcc.Graph(figure=fig)])
        case _:
            pass


@callback(
    Output(component_id="tab-inconsis-df-content", component_property="children"),
    Output(component_id="inconsis-zone", component_property="options"),
    Output(component_id="inconsis-zone", component_property="value"),
    Output(component_id="inconsis-woreda", component_property="options"),
    Output(component_id="inconsis-woreda", component_property="value"),
    Input(component_id="datasets-list", component_property="value"),
    Input(component_id="inconsis-region", component_property="value"),
    Input(component_id="inconsis-zone", component_property="value"),
    Input(component_id="inconsis-woreda", component_property="value"),
)
def compute_inconsis_df(dataset, region, zone, woreda):  # , level, type, ownership):

    match dataset:
        case "EPI":
            df = epi_inconsis_df.select(
                [
                    "hf_name",
                    "region",
                    "zone",
                    "woreda",
                    "level",
                    "hf_type",
                    "ownership",
                    "period",
                    "bcg",
                    "ipv",
                    "penta1",
                    "penta3",
                    "penta_all_ages",
                    "mcv1",
                    "mcv_all_ages",
                    "rota2",
                    "full_vacc",
                ]
            )
        case _:
            raise ValueError("Selected dataset not found!")

    zones = compute_inconsis_zones(df, [region])
    woredas = compute_inconsis_woredas(df, [region], [zone])
    # breakpoint()

    df2 = df.filter(
        pl.col("region").is_in([region]), pl.col("zone").is_in([zone]), pl.col("woreda").is_in([woreda])
    )  # .filter(pl.col("level").is_in([level]) & pl.col("hf_type").is_in([type]) & pl.col("ownership").is_in([ownership]))

    return (
        [
            dag.AgGrid(
                rowData=df2.to_dicts(),
                columnDefs=[{"field": i} for i in df2.columns if i not in ["region", "zone", "woreda"]],
                defaultColDef={"filter": True, "sortable": True, "floatingFilter": True},
                persistence=True,
            )
        ],
        zones,
        zone,
        woredas,
        woreda,
    )  # df.to_dicts(), [{"field": i} for i in df.columns]
