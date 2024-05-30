import os
import asyncio
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

# Define a function to load the dataset asynchronously
async def load_dataset():
    # Define the absolute path to the Parquet file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'subset_selected_events.parquet')
    # Read the Parquet file into a pandas DataFrame
    subset_selected_events = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return subset_selected_events

# Define a function to create the scatter plot layout
async def line_chart_1_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()
    
    # Convert 't0' column to datetime type
    subset_selected_events['t0'] = pd.to_datetime(subset_selected_events['t0'])

    # Extract the date from the t0 column
    subset_selected_events['t0_date'] = subset_selected_events['t0'].dt.date

    # Group by t0_date and eventtype_trip, then count the number of events in each group
    event_counts = subset_selected_events.groupby(['t0_date', 'eventtype_trip']).size().reset_index(name='event_count')

    # Create an interactive line plot with Plotly Express
    scatter_figure = px.line(event_counts, x='t0_date', y='event_count', color='eventtype_trip', title='Total Number of Events Over Time',
                  labels={'t0_date': 'Date', 'event_count': 'Total Number of Events', 'eventtype_trip': 'Event Type'})

    # Define layout for the scatter plot
    layout = html.Div([
        dcc.Graph(
            id='scatter-plot',
            figure=scatter_figure,
            style={'marginLeft': '25px', 'marginRight': '25px'}
        ),
        html.P("Conclusions:", style={'font-weight': 'bold', 'margin-top': '20px', 'margin-left': '50px'}),
        html.Ul([
            html.Li('"P002 - Aggression - fight - rape", "P020 - Intoxication alcohol" and "P021 - Intoxication drugs" interventions are common on January 1.'),
            html.Li('"P010 - Respiratory problems" interventions increase around November 15, peak on December 15, and return to baseline around January 26.'),
            html.Li('"P032 - Allergic reactions" interventions increase around June 5, peak on July 24, and return to baseline around September 22.'),
            html.Li('"P036 - Heat stroke - solar stroke" interventions mainly take place between May and September.'),
            html.Li('"P072 - Sick child < 15 years with fever" interventions increase around November 8, peak on December 19, and return to baseline around January 6.'),
            html.Li('"P080 - COVID-19" interventions come in waves. There is an increase from June 6, decrease from July 18, increase from September 13, decrease from October 5, increase from November 26, decrease from December 19, increase from January 19, decrease from March 9 until May 17.'),
        ], style={'margin-left': '50px', 'margin-right': '70px', 'text-align': 'justify'})
    ])

    return layout
