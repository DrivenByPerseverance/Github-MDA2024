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

# Define a function to create the heatmap layout
async def map_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()

    # Plot the heatmap map
    fig = px.density_mapbox(interventions_dataset, lat='latitude_intervention', lon='longitude_intervention', radius=2,
                             center=dict(lat=50.5, lon=4.35), zoom=5, mapbox_style="carto-positron",
                             title="Heatmap of Interventions by Province")

    # Define layout for the heatmap
    layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return layout
