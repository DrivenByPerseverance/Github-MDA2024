import asyncio
from dash import html, dcc
import plotly.express as px
import pandas as pd
import os

# LOAD DATA FROM FOLDER
"""
# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_line_charts.parquet'
    # Read the Parquet file into a pandas DataFrame
    subset_selected_events = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return subset_selected_events
"""

# LOAD DATA FROM S3 BUCKET
# Define a function to load the dataset asynchronously with caching
async def load_dataset(cache_dir='cache'):
    # Define the filename
    filename = 'subset_line_charts.parquet'
    
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, filename)
    
    # Check if the file is already cached locally
    if os.path.exists(local_path):
        print("Loading subset_line_charts.parquet from cache")
        subset_selected_events = pd.read_parquet(local_path, engine='pyarrow')
    else:
        # File path to S3 bucket
        file_path = 's3://mda2024public/CLEANED/subset_line_charts.parquet'
        
        # Read the Parquet file from S3 into a pandas DataFrame
        print("Downloading subset_line_charts.parquet from S3")
        subset_selected_events = pd.read_parquet(file_path, engine='pyarrow')
        
        # Cache the dataset locally
        subset_selected_events.to_parquet(local_path, engine='pyarrow')
    
    # Simulate data loading time
    await asyncio.sleep(1)
    return subset_selected_events

# Define a function to create the line chart layout
async def line_chart_2_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Group by t0_Hour and count the number of events for each hour
    hourly_counts = subset_selected_events.groupby(['t0_Hour', 'eventtype_trip']).size().reset_index(name='event_count')

    # Plot the total events per t0_Hour using Plotly Express
    fig = px.line(hourly_counts, x='t0_Hour', y='event_count', color='eventtype_trip', title='Total Number of Events per Hour')
    fig.update_xaxes(title='Hour of the Day')
    fig.update_yaxes(title='Total Number of Events')

    # Define layout for the line chart
    layout = html.Div([
        dcc.Graph(
            id='line-chart',
            figure=fig,
            style={'marginLeft': '25px', 'marginRight': '25px'}
        ),
        html.P("Conclusions:", style={'font-weight': 'bold', 'margin-top': '20px', 'margin-left': '50px'}),
        html.Ul([
            html.Li('"P002 - Aggression - fight - rape" interventions mainly take place around 9 pm.'),
            html.Li('"P003 - Cardiac arrest” interventions mainly take place around 8-10 am and a second lower peak occurs around 6 pm.'),
            html.Li('"P010 - Respiratory problems" interventions mainly take place around 10 am.'),
            html.Li('"P012 - Non-traumatic abdominal pain" interventions mainly take place around 9 am.'),
            html.Li('"P013 - Non-traumatic back pain" interventions mainly take place around 9-10 am.'),
            html.Li('"P020 - Intoxication alcohol" interventions mainly take place around 2 am.'),
            html.Li('"P022 - Intoxication medication" interventions mainly take place around 7 pm.'),
            html.Li('"P029 - Obstruction of the respiratory tract" interventions mainly occur around 12 noon and a second lower peak occurs around 6 pm.'),
            html.Li('"P031 - Psychiatric problem" interventions mainly take place around 8 pm.'),
            html.Li('"P032 - Allergic reactions" interventions mainly take place between 12 noon and 8 pm.'),
            html.Li('"P067 - Social problem" interventions mainly take place around 11 pm.'),
            html.Li('"P080 - COVID-19" interventions mainly take place around 11 am or 12 pm.'),
            html.Li('"P097 - Collocation (planned)" interventions mainly take place around 3-4 pm.')
        ], style={'margin-left': '50px', 'margin-right': '70px', 'text-align': 'justify'})
    ])

    return layout

async def update_line_chart():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Group by t0_Hour and count the number of events for each hour
    hourly_counts = subset_selected_events.groupby(['t0_Hour', 'eventtype_trip']).size().reset_index(name='event_count')

    # Plot the total events per t0_Hour using Plotly Express
    fig = px.line(hourly_counts, x='t0_Hour', y='event_count', color='eventtype_trip', title='Total Number of Events per Hour')
    fig.update_xaxes(title='Hour of the Day')
    fig.update_yaxes(title='Total Number of Events')

    return fig



