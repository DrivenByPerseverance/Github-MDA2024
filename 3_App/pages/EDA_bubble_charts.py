import asyncio
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_cardiac.parquet'
    # Read the Parquet file into a pandas DataFrame
    interventions_dataset = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return interventions_dataset

# Define a function to create the bubble chart layout
async def bubble_chart_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()

    # Group by longitude and latitude, and count the number of interventions
    grouped_df = interventions_dataset.groupby(['longitude_intervention', 'latitude_intervention']).size().reset_index(name='Number of Interventions')

    # Plot the bubble plot map
    fig = px.scatter_mapbox(grouped_df, lat="latitude_intervention", lon="longitude_intervention",
                            size="Number of Interventions", color="Number of Interventions",
                            hover_name="Number of Interventions",
                            zoom=5, height=600, size_max=10)

    # Customize the map layout
    fig.update_layout(mapbox_style="carto-positron",
                      title="Bubble Plot Map of Interventions by Province",
                      mapbox_zoom=7, mapbox_center={"lat": 50.5, "lon": 4.35},
                      margin={"r":0,"t":50,"l":0,"b":0})

    # Define layout for the bubble chart
    layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return layout
