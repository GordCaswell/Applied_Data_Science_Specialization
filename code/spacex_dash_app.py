# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children = [
        html.H1(
            'SpaceX Launch Records Dashboard',
            style = {
                'textAlign': 'center',
                'color': '#503D36',
                'font-size': 40
            }
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id = 'site-dropdown',
            options = [
                {
                    'label': 'All Sites',
                    'value': 'ALL'
                },
                {
                    'label': 'CCAFS LC-40',
                    'value': 'CCAFS LC-40'
                },
                {
                    'label': 'CCAFS SLC-40',
                    'value': 'CCAFS SLC-40'
                },
                {
                    'label': 'KSC LC-39A',
                    'value': 'KSC LC-39A'
                },
                {
                    'label': 'VAFB SLC-4E',
                    'value': 'VAFB SLC-4E'
                }
            ],
            value = 'ALL',
            placeholder = "Select a Launch Site here",
            searchable = True
        ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(
            dcc.Graph(
                id = 'success-pie-chart'
            )
        ),
        html.Br(),
        html.P(
            "Payload range (Kg):"
        ),

        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id = 'payload-slider',
            min = 0,
            max = 10000,
            step = 1000,
            marks = {
                0: '0',
                2500: '2500',
                5000: '5000',
                7500: '7500',
                10000: '10000'
            },
            value = [
                min_payload,
                max_payload
            ]
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(
                id = 'success-payload-scatter-chart'
            )
        ),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(
        component_id = 'success-pie-chart',
        component_property = 'figure'
    ),
    Input(
        component_id = 'site-dropdown',
        component_property = 'value'
    )
)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        pie_title_suffix = 'By Site'
        fig = px.pie(
            spacex_df,
            values = 'class',
            names = 'Launch Site',
        )
    else:
        pie_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        successful_launches_count = pie_data['class'].eq(1).sum()
        failed_launches_count = pie_data['class'].eq(0).sum()
        pie_title_suffix = 'for site ' + entered_site
        fig = px.pie(
            pie_data,
            values = [
                failed_launches_count,
                successful_launches_count
            ],
            names = {
                0: 'Failure',
                1: 'Success'
            },
            color = [
                0,
                1
            ],
            color_discrete_map = {
                0: 'red',
                1: 'green'
            }
        )
    fig.update_traces(
        textposition = 'inside',
        textinfo = 'percent+value'
    )
    fig.update_layout(
        title = 'Total Successful Launches ' + pie_title_suffix
    )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(
        component_id = 'success-payload-scatter-chart',
        component_property = 'figure'
    ),
    [
        Input(
            component_id = 'site-dropdown',
            component_property = 'value'
        ),
        Input(
            component_id = 'payload-slider',
            component_property = 'value'
        )
    ]
)

def get_scatter_chart(entered_site, selected_payload_range):
    low, high = selected_payload_range
    if entered_site == 'ALL':
        mask = spacex_df['Payload Mass (kg)'].between(low, high)
        df = spacex_df[mask]
        scatter_title_suffix = 'all Sites'
    else:
        scatter_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        mask = scatter_data['Payload Mass (kg)'].between(low, high)
        df = scatter_data[mask]
        scatter_title_suffix = 'site ' + entered_site
    fig = px.scatter(
        df,
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = 'Correlation between Payload and Success for ' + scatter_title_suffix
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
