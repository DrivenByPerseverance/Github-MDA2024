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

# Define a function to create the bar chart layout
async def bar_chart_layout():
    # Load the dataset asynchronously
    interventions_dataset = await load_dataset()

    # Convert columns t0, t1, t2, t3, t4, t5, t6, t7 to datetime format with UTC timezone
    interventions_dataset[['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']] = interventions_dataset[['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S.%f')

    # Calculate the time differences in minutes
    interventions_dataset['T0 -> T1'] = (interventions_dataset['t1'] - interventions_dataset['t0']).dt.total_seconds() / 60
    interventions_dataset['T1 -> T2'] = interventions_dataset['T0 -> T1'] + (interventions_dataset['t2'] - interventions_dataset['t1']).dt.total_seconds() / 60
    interventions_dataset['T2 -> T3'] = interventions_dataset['T1 -> T2'] + (interventions_dataset['t3'] - interventions_dataset['t2']).dt.total_seconds() / 60
    interventions_dataset['T3 -> T4'] = interventions_dataset['T2 -> T3'] + (interventions_dataset['t4'] - interventions_dataset['t3']).dt.total_seconds() / 60
    interventions_dataset['T4 -> T5'] = interventions_dataset['T3 -> T4'] + (interventions_dataset['t5'] - interventions_dataset['t4']).dt.total_seconds() / 60
    interventions_dataset['T5 -> T6'] = interventions_dataset['T4 -> T5'] + (interventions_dataset['t6'] - interventions_dataset['t5']).dt.total_seconds() / 60
    interventions_dataset['T6 -> T7'] = interventions_dataset['T5 -> T6'] + (interventions_dataset['t7'] - interventions_dataset['t6']).dt.total_seconds() / 60

    # Group by vector type and calculate the mean time differences for each group
    grouped = interventions_dataset.groupby('vector_type').mean()

    # Create traces for each vector type
    data = []
    for vector_type, row in grouped.iterrows():
        trace = go.Bar(x=['T0 -> T1', 'T1 -> T2', 'T2 -> T3', 'T3 -> T4', 'T4 -> T5', 'T5 -> T6', 'T6 -> T7'],
                       y=row[['T0 -> T1', 'T1 -> T2', 'T2 -> T3', 'T3 -> T4', 'T4 -> T5', 'T5 -> T6', 'T6 -> T7']],
                       name=vector_type)
        data.append(trace)

    # Create layout
    layout = go.Layout(title='Average Time Differences by Vector Type',
                       xaxis=dict(title='t Columns'),
                       yaxis=dict(title='Average Time Difference (minutes)'),
                       barmode='group',  # Add barmode to group bars
                       legend=dict(title='Vector Type'))

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    # Define layout for the bar chart
    bar_chart_layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return bar_chart_layout
