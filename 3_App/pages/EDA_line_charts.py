import asyncio
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_cardiac.parquet'
    # Read the Parquet file into a pandas DataFrame
    interventions_dataset = pd.read_parquet(file_path, engine='pyarrow', columns=['t0_Hour'])
    # Simulate data loading time
    await asyncio.sleep(1)
    return interventions_dataset

# Define a function to create the line chart layout
async def line_chart_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()

    # Group by t0_Hour and count the number of events for each hour
    hourly_counts = interventions_dataset.groupby('t0_Hour').size().reset_index(name='event_count')

    # Plot the total events per t0_Hour using Plotly Express
    fig = px.line(hourly_counts, x='t0_Hour', y='event_count', title='Total Events of XXX per Hour')
    fig.update_xaxes(title='Hour of the Day')
    fig.update_yaxes(title='Total Number of Events')

    # Define layout for the line chart
    layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return layout
