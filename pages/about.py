import dash
from dash import html

import dash_bootstrap_components as dbc

dash.register_page(__name__, name="FeeLoST", path="/")


layout = html.Div(
    id="about-page",
    children=[
        dbc.Row(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("What is the Feedback Loop System (FeeLoST)?"),
                        html.P(
                            "The Feedback Loop System Tool (FeeLoST) allows the monitoring, checking, and validation of routine health facility data and streamline the communication between the reporting health facilities and the administrative / organizational units in Ethiopia. The FeeLoST facilitates automatic loading of the DHIS2 datasets, calculation and visualization of the data and quality metrics. The platform enables the exchange of emails to discuss issues related to the reported data. Therefore, the FeeLoST minimizes the barriers in analysing the quality of the facility health routine data from DHIS2 and increase its quality."
                        ),
                        html.P(
                            "The FeeLoST automates many of the manual processes currently in place in DHIS2 and adds more tools for assessing the quality of DHIS2 data. The FeeLoST provides highly effective dashboards, data quality metrics, and functionalities designed by an interdisciplinary team involving health service providers, IT and M&E specialists, data managers, and key stakeholders at the local, national, and international levels."
                        ),
                        html.P(
                            "The data is hosted in secured in-country cloud infrastructure allowing access to the FeeLoST web platform from health facilities and administrative units all over the country with internet connection."
                        ),
                        html.P("The FeeLoST web platform allows the users to"),
                        html.Ul(
                            [
                                html.Li(
                                    html.A(
                                        "Monitor and review the quality of the DHIS2 data on a regular basis based on a set of standard and customized metrics."
                                    )
                                ),
                                html.Li(
                                    html.A(
                                        "To provide feedback to the health routine data recorder on the quality of the data in the DHIS2 platform. "
                                    )
                                ),
                                html.Li(html.A("To create and share data quality metrics and reports.")),
                                html.Li(
                                    html.A("Store summary statistics for Power BI and other dashboard systems to use.")
                                ),
                            ]
                        ),
                        html.H3("Who are the users of FeeLoST?"),
                        html.P("The FeeLoST is intended to be used by"),
                        html.Ul(
                            [
                                html.Li(
                                    html.A(
                                        "The data managers at the hospitals, health centres, health posts, private clinics, other health facilities. The data managers record the information in DHIS2 on a regular basis. On the FeeLoST platform, the main role of the data recorders is to address identified or possible data quality issues flagged on the platform."
                                    )
                                ),
                                html.Li(
                                    html.A(
                                        "The health officials at different administrative levels, i.e. national, regional, zones, and districts. The data reviewers examine the data on a regular basis, tracking and monitoring quality metrics. They can provide feedback to the data recorders based on their review of the data."
                                    )
                                ),
                                html.Li(
                                    html.A(
                                        "The system administrators regional level IT personnel. They manage the platform, create and support users."
                                    )
                                ),
                            ]
                        ),
                        html.H3("FeeLoST Data Quality Metrics"),
                        html.P(
                            "The FeeLoST data quality metrics are used to automatically flag potential quality issues. There are three categories of data quality metrics: outlier, inconsistency, and missingness"
                        ),
                        html.H5("Outliers"),
                        html.P(
                            "Data outliers refer to individual observations or data points that significantly differ from the majority of the dataset. These anomalies can take the form of unusually high or low values and have the potential to distort statistical analyses and interpretations. Identifying and understanding outliers is critical to assessment of the quality of the health data. We calculate the outliers using three methods."
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    [
                                        html.A(html.B("Metrod 1: using the Interquartile Range (IQR)")),
                                        dcc.Markdown(
                                            """
                                            The IQR is a measure of statistical dispersion defined as $IQR=Q3-Q1$, where $Q3$ is the third quartile and $Q1$ is the first quartile.
                                            - Data points that fall below $Q1 - 1.5 * IQR$ or above $Q3 + 1.5 * IQR$ are often considered **outliers**.
                                            - Data points that fall below $Q1 - 3 * IQR$ or above $Q3 + 3 * IQR$ are often considered **extreme** values.""",
                                            mathjax=True,
                                        ),
                                    ]
                                ),
                                html.Br(),
                                html.Li(
                                    [
                                        html.A(html.B("Metrod 2: using the z-scores")),
                                    ]
                                ),
                                html.Br(),
                                html.Li(
                                    [
                                        html.A(html.B("Metrod 3: using the Thompson Tau Test (TTT)")),
                                    ]
                                ),
                            ]
                        ),
                        html.H3("Contact Us"),
                    ],
                    style={"padding": 25, "width": "95"},
                    # className="all",
                )
            )
        )
    ],
)
