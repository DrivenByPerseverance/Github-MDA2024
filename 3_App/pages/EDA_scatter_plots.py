import asyncio
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd

# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_cardiac.parquet'
    # Read the Parquet file into a pandas DataFrame
    interventions_dataset = pd.read_parquet(file_path, engine='pyarrow', columns=['t0_Hour'])
    # Simulate data loading time
    await asyncio.sleep(1)
    return interventions_dataset

# Define a function to create the scatter plot layout
async def scatter_plot_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()
    
    # Create scatter plot figure
    scatter_figure = go.Figure(
        data=go.Scatter(
            x=interventions_dataset['t0_Hour'],
            y=interventions_dataset['t0_Hour'],
            mode='markers',
            marker=dict(color='blue')
        ),
        layout=dict(
            title='Sample Scatter Plot',
            xaxis=dict(title='X-axis'),
            yaxis=dict(title='Y-axis')
        )
    )

    # Define layout for the scatter plot
    layout = html.Div([
        dcc.Graph(figure=scatter_figure)
    ])

    return layout

