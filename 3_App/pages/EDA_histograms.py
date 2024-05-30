import os
import asyncio
from dash import html, dcc, Input, Output
import plotly.graph_objs as go
import pandas as pd
import calendar

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

# Define a function to convert numeric month to textual format
def numeric_to_textual_month(month):
    return calendar.month_name[int(month)]

# Define a function to update histograms based on the selected option
async def update_histograms(selected_option):
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Filter dataset based on the selected option
    if selected_option == 1:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P002 - Agression - fight - rape']
    elif selected_option == 2:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P003 - Cardiac arrest']
    elif selected_option == 3:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P010 - Respiratory problems']
    elif selected_option == 4:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P020 - Intoxication alcohol']
    elif selected_option == 5:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P021 - Intoxication drugs']
    elif selected_option == 6:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P032 - Allergic reactions']
    elif selected_option == 7:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P036 - Heat stroke - solar stroke']
    elif selected_option == 8:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P072 - Sick child < 15 years with fever']
    elif selected_option == 9:
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P080 - COVID-19']
    else:
        # Add logic for the third option
        filtered_dataset = subset_selected_events  # For example, no filtering
        
    # Group by t0_Day and t0_Month, and count occurrences for year histogram
    grouped_month_day = filtered_dataset.groupby([filtered_dataset['t0_Month'], filtered_dataset['t0_Day']]).size().unstack().fillna(0)
    grouped_month_day.index = grouped_month_day.index.map(numeric_to_textual_month)
    grouped_month_day = grouped_month_day.iloc[::-1]
    heatmap_year = go.Figure(data=go.Heatmap(
        z=grouped_month_day.values,
        x=grouped_month_day.columns,
        y=grouped_month_day.index,
        colorscale='Viridis'
    ))
    heatmap_year.update_layout(
        title='Number of Events by Month and Day',
        xaxis_title='Day',
        yaxis_title='Month'
    )

    # Group by t0_hour and t0_NameDay, and count occurrences for week histogram
    days_of_week_order = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
    grouped_week = filtered_dataset.groupby([filtered_dataset['t0_DayName'], filtered_dataset['t0_Hour']]).size().unstack().fillna(0)
    grouped_week = grouped_week.reindex(days_of_week_order)
    heatmap_week = go.Figure(data=go.Heatmap(
        z=grouped_week.values,
        x=grouped_week.columns,
        y=grouped_week.index,
        colorscale='Viridis'
    ))
    heatmap_week.update_layout(
        title='Number of Events by Name Day and Hour',
        xaxis_title='Hour',
        yaxis_title='Name Day'
    )

    return heatmap_year, heatmap_week

# Define a function to create the heatmap layout
async def histogram_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Group by t0_Day and t0_Month, and count occurrences
    grouped_month_day = subset_selected_events.groupby([subset_selected_events['t0_Month'], subset_selected_events['t0_Day']]).size().unstack().fillna(0)

    # Convert numeric month to textual format and reverse the order of months
    grouped_month_day.index = grouped_month_day.index.map(numeric_to_textual_month)
    grouped_month_day = grouped_month_day.iloc[::-1]

    # Create the heatmap for yearly data
    heatmap_year = go.Figure(data=go.Heatmap(
        z=grouped_month_day.values,
        x=grouped_month_day.columns,
        y=grouped_month_day.index,
        colorscale='Viridis'
    ))

    # Update layout for yearly heatmap
    heatmap_year.update_layout(
        title='Number of Events by Month and Day',
        xaxis_title='Day',
        yaxis_title='Month'
    )

    # Define the order of the days of the week
    days_of_week_order = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']

    # Group by t0_hour and t0_NameDay, and count occurrences
    grouped_week = subset_selected_events.groupby([subset_selected_events['t0_DayName'], subset_selected_events['t0_Hour']]).size().unstack().fillna(0)

    # Reorder the rows according to the specified order of days
    grouped_week = grouped_week.reindex(days_of_week_order)

    # Create a heatmap for weekly data
    heatmap_week = go.Figure(data=go.Heatmap(
        z=grouped_week.values,
        x=grouped_week.columns,
        y=grouped_week.index,
        colorscale='Viridis'
    ))

    # Update layout for weekly heatmap
    heatmap_week.update_layout(
        title='Number of Events by Name Day and Hour',
        xaxis_title='Hour',
        yaxis_title='Name Day'
    )
    
    # Define layout for both heatmaps
    layout = html.Div([
        html.Div([
            dcc.Graph(id='histogram-year', figure=heatmap_year)
        ], style={'margin-left': '40px', 'width': '45%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='histogram-week', figure=heatmap_week)
        ], style={'margin-right': '40px', 'width': '45%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='option-dropdown',
                options=[
                    {'label': 'P002 - Agression - fight - rape', 'value': 1},
                    {'label': 'P003 - Cardiac arrest', 'value': 2},
                    {'label': 'P010 - Respiratory problems', 'value': 3},
                    {'label': 'P020 - Intoxication alcohol', 'value': 4},
                    {'label': 'P021 - Intoxication drugs', 'value': 5},
                    {'label': 'P032 - Allergic reactions', 'value': 6},
                    {'label': 'P036 - Heat stroke - solar stroke', 'value': 7},
                    {'label': 'P072 - Sick child < 15 years with fever', 'value': 8},
                    {'label': 'P080 - COVID-19', 'value': 9}
                ],
                value=1,
                style={'width': '80%', 'margin': 'auto'}
            ),
        ], style={'width': '100%', 'padding': '20px 0'}),
        html.P("Conclusions:", style={'font-weight': 'bold', 'margin-top': '20px', 'margin-left': '50px'}),
        html.Ul([
            html.Li('"P002 - Aggression - fight - rape" interventions are common on January 1. In addition, those interventions mainly take place on Saturdays and Sundays around 2 am.'),
            html.Li('“P003 - Cardiac arrest” interventions mainly take place in december.'),
            html.Li('"P010 - Respiratory problems" mainly occur in December and January. This increase is probably due to the cold, dry air during the winter. In addition, the interventions mainly take place around 10 am.'),
            html.Li('"P020 - Intoxication alcohol" and "P021 - Intoxication drugs" interventions are again common on January 1. Those interventions are probably due to the celebration of New Year\'s Eve. In addition, those interventions mainly take place around 2 am. Many more interventions take place during the weekends than during the week.'),
            html.Li('"P032 - Allergic reactions" interventions mainly occur in July and August during the afternoon and early evening.'),
            html.Li('"P036 - Heat stroke - solar stroke" interventions mainly occur in the summer months of June, July, and August. In addition, the interventions mainly take place during the afternoon.'),
            html.Li('"P072 - Sick child < 15 years with fever" interventions mainly occur in December. In addition, the interventions mainly take place in the evening.'),
            html.Li('"P080 - COVID-19" interventions come in waves. The months with the most interventions are July, October and December. In addition, the interventions mainly take place around 11 am or 12 pm.')
        ], style={'margin-left': '50px', 'margin-right': '70px', 'text-align': 'justify'})
    ], id='histograms-figure')

    return layout