import dash
from dash import html, dcc, dash_table, callback, Input, Output


import dash_bootstrap_components as dbc

import polars as pl

dash.register_page(__name__, name="FeeLoST")


hf_list_df = pl.read_csv("./data/input/hf_list_df.csv")

epi_df = pl.read_csv("./data/input/epi_df.csv")


datasets_list = ["hf_list", "epi"]
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

layout = html.Div(
    id="datasets",
    children=[
        html.Div(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
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
                                html.Label("Quarters of interest"),
                                dcc.Dropdown(id="selected-quarters", options=quarters, value="All", multi=True),
                                html.Br(),
                                html.Label("Months of interest"),
                                dcc.Dropdown(id="selected-months", options=months, value="All", multi=True),
                            ],
                        )
                    ]
                )
            ),
            style={"padding": 10, "flex": 1},
        ),
        html.Div(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            id="datatable-id",
                        ),
                    ],
                ),
            ),
            style={"padding": 10, "flex": 7},
        ),
    ],
    style={"display": "flex", "flexDirection": "row", "gap": "5px", "width": "100%"},
    # className="all",
)


@callback(
    # Output("datatable-id", "columns"),
    Output("datatable-id", "children"),
    Input("datasets-list", "value"),
    Input("number-rows", "value"),
    Input("selected-years", "value"),
    Input("selected-months", "value"),
)
def datasets_server(datasets_names, number_rows, selected_years, selected_months):
    match datasets_names:
        case "hf_list":
            df = hf_list_df.head(number_rows)
        case "epi":
            if "All" in selected_months or len(selected_months) == 0:
                months_selected = months
            else:
                months_selected = selected_months

            df = (
                epi_df.filter(pl.col("year").is_between(selected_years[0], selected_years[1]))
                .filter(pl.col("month").is_in(months_selected))
                .head(number_rows)
            )

    return dash_table.DataTable(
        data=df[:number_rows].to_dicts(),  # to_dicts() equivalent to the option "records" for pandas' to_dict()
        columns=[{"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True} for i in df.columns],
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="multi",
        page_action="native",
        page_current=0,
        # page_size=20,
        style_table={
            "overflowX": "auto",
            # "maxWidth": "900px",
        },
        # style_cell={
        #     # "overflow": "hidden",
        #     # "textOverflow": "ellipsis",
        #     # "minWidth": "180px",
        #     # "width": "180px",
        #     # "maxWidth": "180px",
        # },
    )
