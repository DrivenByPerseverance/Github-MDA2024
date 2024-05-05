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
async def correlation_heatmap_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()
    
    # Assuming df_interventions1 is your DataFrame
    selected_columns = ['vector_type', 'eventlevel_trip']

    # Selecting the relevant columns
    df_selected = interventions_dataset[selected_columns]

    # Encoding categorical variables using one-hot encoding
    df_encoded = pd.get_dummies(df_selected)

    # Calculating the correlation matrix
    correlation_matrix = df_encoded.corr()

    # Select the dummy variables of "vector_type" on the y-axis and "eventlevel_trip" on the x-axis
    correlation_subset = correlation_matrix.loc[df_encoded.columns[df_encoded.columns.str.startswith('vector_type')],
                                                df_encoded.columns[df_encoded.columns.str.startswith('eventlevel_trip')]]

    # Create a heatmap using Plotly
    heatmap = go.Heatmap(
        z=correlation_subset.values,
        x=correlation_subset.columns,
        y=correlation_subset.index,
        colorscale='RdBu',
        zmin=-1, zmax=1
    )

    # Create layout for the heatmap
    layout = html.Div([
        dcc.Graph(figure=go.Figure(data=[heatmap], layout=go.Layout(
            title='Correlation Matrix between vector_type and eventlevel_trip',
            xaxis=dict(title='eventlevel_trip'),
            yaxis=dict(title='vector_type'),
            margin=dict(l=140, r=40, t=80, b=40),
        )))
    ])

    return layout

