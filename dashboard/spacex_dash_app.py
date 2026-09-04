import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the SpaceX launch dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

print(spacex_df.columns.tolist())
print(spacex_df.dtypes)

# Display the first few rows
print(spacex_df.head())

# Create the Dash application
app = dash.Dash(__name__)

# Create the dashboard layout
app.layout = html.Div([
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={'textAlign': 'center'}
    ),

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    dcc.Graph(id='success-pie-chart'),

html.Br(),

html.Label("Payload Mass (kg):"),

dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    value=[0, 10000],
    marks={
        0: '0',
        1000: '1000',
        2000: '2000',
        3000: '3000',
        4000: '4000',
        5000: '5000',
        6000: '6000',
        7000: '7000',
        8000: '8000',
        9000: '9000',
        10000: '10000'
    }
),

html.Br(),

dcc.Graph(id='success-payload-scatter-chart')
])

# Callback to update the success pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_pie_chart(entered_site, payload_range):

    min_payload, max_payload = payload_range

    # Filter by payload mass
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= min_payload) &
        (spacex_df['Payload Mass (kg)'] <= max_payload)
    ]

    # Filter by launch site if a specific site is selected
    if entered_site != 'ALL':
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

    # Create pie chart
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs. Failure for {entered_site}'
        )

    return fig

# Callback to update the payload vs. success scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, payload_range):

    min_payload, max_payload = payload_range

    # Filter by payload mass
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= min_payload) &
        (spacex_df['Payload Mass (kg)'] <= max_payload)
    ]

    # Filter by launch site if a specific site is selected
    if entered_site != 'ALL':
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs. Launch Success'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)