# Copy and paste the below command to the terminal.
# pip install pandas dash

# Run the following wget command line in the terminal to download dataset as spacex_launch_dash.csv
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "All Sites"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
            ],
            value="All Sites",
            placeholder="Select a launch site",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0",
                1000: "1000",
                2000: "2000",
                3000: "3000",
                4000: "4000",
                5000: "5000",
                6000: "6000",
                7000: "7000",
                8000: "8000",
                9000: "9000",
                10000: "10000",
            },
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    spacex_1_df = spacex_df
    if entered_site == "All Sites":
        fig = px.pie(spacex_1_df, values="class", names="Launch Site", title="Total Successful Launches by Site")
        return fig
    else:
        spacex_1_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        spacex_1_df = spacex_1_df.groupby(["Launch Site", "class"]).size().reset_index(name="class count")
        fig = px.pie(
            spacex_1_df, values="class count", names="class", title=f"Total Successful Launches for {entered_site}"
        )
        return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def scatter(entered_site, payload):
    spacex_1_df = spacex_df[spacex_df["Payload Mass (kg)"].between(payload[0], payload[1])]

    if entered_site == "All Sites":
        fig = px.scatter(
            spacex_1_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Success count on Payload mass for all sites",
        )
        return fig
    else:
        fig = px.scatter(
            spacex_1_df[spacex_1_df["Launch Site"] == entered_site],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Success count on Payload mass for {entered_site}",
        )
        return fig


if __name__ == "__main__":
    app.run_server()
