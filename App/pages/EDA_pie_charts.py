import asyncio
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import os

# LOAD DATA FROM FOLDER
"""
# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_selected_events.parquet'
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
    filename = 'subset_selected_events.parquet'
    
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, filename)
    
    # Check if the file is already cached locally
    if os.path.exists(local_path):
        print("Loading subset_selected_events.parquet from cache")
        subset_selected_events = pd.read_parquet(local_path, engine='pyarrow')
    else:
        # File path to S3 bucket
        file_path = 's3://mda2024public/CLEANED/subset_selected_events.parquet'
        
        # Read the Parquet file from S3 into a pandas DataFrame
        print("Downloading subset_selected_events.parquet from S3")
        subset_selected_events = pd.read_parquet(file_path, engine='pyarrow')
        
        # Cache the dataset locally
        subset_selected_events.to_parquet(local_path, engine='pyarrow')
    
    # Simulate data loading time
    await asyncio.sleep(1)
    return subset_selected_events


# Define a function to create the pie chart layout
async def update_pie_charts(selected_option):
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Filter dataset based on the selected option
    if selected_option == 'P002 - Agression - fight - rape':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P002 - Agression - fight - rape']
    elif selected_option == 'P003 - Cardiac arrest':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P003 - Cardiac arrest']
    elif selected_option == 'P010 - Respiratory problems':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P010 - Respiratory problems']
    elif selected_option == 'P020 - Intoxication alcohol':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P020 - Intoxication alcohol']
    elif selected_option == 'P021 - Intoxication drugs':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P021 - Intoxication drugs']
    elif selected_option == 'P032 - Allergic reactions':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P032 - Allergic reactions']
    elif selected_option == 'P036 - Heat stroke - solar stroke':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P036 - Heat stroke - solar stroke']
    elif selected_option == 'P072 - Sick child < 15 years with fever':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P072 - Sick child < 15 years with fever']
    elif selected_option == 'P080 - COVID-19':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P080 - COVID-19']
    else:
        # Add logic for the third option
        filtered_dataset = subset_selected_events  # For example, no filtering
    
    # Calculate the count of interventions by province
    province_counts = filtered_dataset['province_intervention'].value_counts()

    # Create pie chart figure
    pie_figure = go.Figure(
        data=go.Pie(
            labels=province_counts.index,
            values=province_counts.values,
            hole=0.3,  # Set hole size
            marker_colors=['red', 'blue', 'green', 'orange', 'purple']  # Set slice colors
        ),
        layout=dict(
            title='Distribution of Interventions for "{}" by Province'.format(selected_option)
        )
    )

    return pie_figure



# Define a function to create the heatmap layout
async def pie_charts_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Calculate the count of interventions by province
    province_counts = subset_selected_events['province_intervention'].value_counts()

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


    # Define layout for pie chart
    layout = html.Div([
        html.Div([
            dcc.Graph(id='pie-chart', figure=pie_figure)
        ],),
        html.Div([
            dcc.Dropdown(
                id='option-dropdown',
                options=[
                    {'label': 'P002 - Agression - fight - rape', 'value': 'P002 - Agression - fight - rape'},
                    {'label': 'P003 - Cardiac arrest', 'value': 'P003 - Cardiac arrest'},
                    {'label': 'P010 - Respiratory problems', 'value': 'P010 - Respiratory problems'},
                    {'label': 'P020 - Intoxication alcohol', 'value': 'P020 - Intoxication alcohol'},
                    {'label': 'P021 - Intoxication drugs', 'value': 'P021 - Intoxication drugs'},
                    {'label': 'P032 - Allergic reactions', 'value': 'P032 - Allergic reactions'},
                    {'label': 'P036 - Heat stroke - solar stroke', 'value': 'P036 - Heat stroke - solar stroke'},
                    {'label': 'P072 - Sick child < 15 years with fever', 'value': 'P072 - Sick child < 15 years with fever'},
                    {'label': 'P080 - COVID-19', 'value': 'P080 - COVID-19'}
                ],
                value='P002 - Agression - fight - rape',
                style={'width': '80%', 'margin': 'auto'}
            ),
        ], style={'width': '100%', 'padding': '20px 0'})
    ], id='pie-charts-figure')

    return layout
