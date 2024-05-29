import asyncio
from dash import html, dcc, callback_context
import plotly.express as px
import pandas as pd

# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_cardiac.parquet'
    # Read the Parquet file into a pandas DataFrame
    subset_selected_events = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return subset_selected_events


async def update_bubble_map(start_date, end_date):
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Ensure 't0' column is converted to datetime type
    subset_selected_events['t0'] = pd.to_datetime(subset_selected_events['t0'])

    # Filter dataset based on selected date range
    filtered_dataset = subset_selected_events[(subset_selected_events['t0'] >= start_date) & (subset_selected_events['t0'] <= end_date)]

    # Group by longitude and latitude, and count the number of interventions
    grouped_df = filtered_dataset.groupby(['longitude_intervention', 'latitude_intervention']).size().reset_index(name='Number of Interventions')

    # Plot the bubble plot map
    bubble_map = px.scatter_mapbox(grouped_df, lat="latitude_intervention", lon="longitude_intervention",
                            size="Number of Interventions", color="Number of Interventions",
                            hover_name="Number of Interventions",
                            zoom=5, height=600, size_max=10)

    # Customize the map layout
    bubble_map.update_layout(mapbox_style="carto-positron",
                      title="Bubble Map of 'P003 - Cardiac Arrest Interventions'",
                      mapbox_zoom=6.8, mapbox_center={"lat": 50.5, "lon": 4.35},
                      margin={"r":0,"t":50,"l":0,"b":0})

    return bubble_map


# Define a function to create the bubble chart layout
async def bubble_map_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Ensure 't0' column is converted to datetime type
    subset_selected_events['t0'] = pd.to_datetime(subset_selected_events['t0'])

    # Callback to filter data based on date range selection
    ctx = callback_context
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'date-picker-range.value':
        start_date, end_date = ctx.triggered[0]['value']
        filtered_dataset = subset_selected_events[(subset_selected_events['t0'] >= start_date) & (subset_selected_events['t0'] <= end_date)]
    else:
        filtered_dataset = subset_selected_events

    # Group by longitude and latitude, and count the number of interventions
    grouped_df = filtered_dataset.groupby(['longitude_intervention', 'latitude_intervention']).size().reset_index(name='Number of Interventions')

    # Plot the bubble plot map
    bubble_map = px.scatter_mapbox(grouped_df, lat="latitude_intervention", lon="longitude_intervention",
                            size="Number of Interventions", color="Number of Interventions",
                            hover_name="Number of Interventions",
                            zoom=5, height=600, size_max=10)

    # Customize the map layout
    bubble_map.update_layout(mapbox_style="carto-positron",
                      title="Bubble Map of 'P003 - Cardiac Arrest' Interventions",
                      mapbox_zoom=6.8, mapbox_center={"lat": 50.5, "lon": 4.35},
                      margin={"r":0,"t":50,"l":0,"b":0})

    # Define layout for the bubble chart
    layout = html.Div([
        html.Div([
            dcc.Graph(
                id='bubble-map',
                figure=bubble_map,
                style={'marginTop': '15px', 'marginLeft': '25px', 'marginRight': '25px'}  # Add left margin of 25 pixels
            ),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=subset_selected_events['t0'].min(),
                end_date=subset_selected_events['t0'].max(),
                display_format='YYYY-MM-DD',
            )
        ], style={'textAlign': 'center'})  # Center align the components
    ])

    return layout

