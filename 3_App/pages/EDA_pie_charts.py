import asyncio
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd

# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_cardiac.parquet'
    # Read the Parquet file into a pandas DataFrame
    interventions_dataset = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return interventions_dataset

# Define a function to create the pie chart layout
async def pie_chart_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()

    # Calculate the count of interventions by province
    province_counts = interventions_dataset['province_intervention'].value_counts()

    # Create pie chart figure
    pie_figure = go.Figure(
        data=go.Pie(
            labels=province_counts.index,
            values=province_counts.values,
            hole=0.3,  # Set hole size
            marker_colors=['red', 'blue', 'green', 'orange', 'purple']  # Set slice colors
        ),
        layout=dict(
            title='Distribution of Interventions for "P002 - Agression - fight - rape" by Province'
        )
    )

    # Define layout for the pie chart
    layout = html.Div([
        dcc.Graph(figure=pie_figure)
    ])

    return layout

