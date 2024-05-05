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

# Define a function to create the heatmap layout
async def histogram_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()

    # Define the order of the days of the week
    days_of_week_order = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']

    # Group by t0_hour and t0_NameDay, and count occurrences
    grouped = interventions_dataset.groupby([interventions_dataset['t0_DayName'], interventions_dataset['t0_Hour']]).size().unstack().fillna(0)

    # Reorder the rows according to the specified order of days
    grouped = grouped.reindex(days_of_week_order)

    # Create a heatmap
    heatmap_figure = go.Figure(data=go.Heatmap(
        z=grouped.values,
        x=grouped.columns,
        y=grouped.index,
        colorscale='Viridis'
    ))

    # Update layout
    heatmap_figure.update_layout(
        title='Number of Events by Hour and Name Day',
        xaxis_title='Hour',
        yaxis_title='Name Day'
    )

    # Define layout for the heatmap
    layout = html.Div([
        dcc.Graph(figure=heatmap_figure)
    ])

    return layout

