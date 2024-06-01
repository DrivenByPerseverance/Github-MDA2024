import asyncio
import pandas as pd
import plotly.express as px
from dash import html, dcc
import os

# LOAD DATA FROM FOLDER
"""
# Define a function to load the dataset asynchronously
async def load_dataset():
    # File path to folder
    file_path = '1_Data/CLEANED/subset_selected_events.parquet'
    # File path to S3 bucket
    file_path = 's3://mda2024public/CLEANED/subset_selected_events.parquet'
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

# Define the order of months and days
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Function to plot interventions for a specific event type
async def update_bar_charts(selected_option):
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()
    
    # Filter dataset based on the selected option
    if selected_option == 'P002 - Agression - fight - rape':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P002 - Agression - fight - rape'].copy()
    elif selected_option == 'P003 - Cardiac arrest':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P003 - Cardiac arrest'].copy()
    elif selected_option == 'P010 - Respiratory problems':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P010 - Respiratory problems'].copy()
    elif selected_option == 'P020 - Intoxication alcohol':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P020 - Intoxication alcohol'].copy()
    elif selected_option == 'P021 - Intoxication drugs':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P021 - Intoxication drugs'].copy()
    elif selected_option == 'P032 - Allergic reactions':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P032 - Allergic reactions'].copy()
    elif selected_option == 'P036 - Heat stroke - solar stroke':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P036 - Heat stroke - solar stroke'].copy()
    elif selected_option == 'P072 - Sick child < 15 years with fever':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P072 - Sick child < 15 years with fever'].copy()
    elif selected_option == 'P080 - COVID-19':
        filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == 'P080 - COVID-19'].copy()
    else:
        # Add logic for the third option
        filtered_dataset = subset_selected_events.copy()  # For example, no filtering
    
    # Convert columns t0, t1, t2, t3, t4, t5, t6, t7 to datetime format with UTC timezone awareness
    cols_to_convert = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']
    filtered_dataset[cols_to_convert] = filtered_dataset[cols_to_convert].apply(lambda x: pd.to_datetime(x, utc=True))

    # Group by month and Name Day, and count occurrences
    grouped = filtered_dataset.groupby([filtered_dataset['t0'].dt.month_name(), filtered_dataset['t0'].dt.day_name()]).size().unstack().fillna(0)

    # Flatten the DataFrame to have a single index
    grouped_flat = grouped.reset_index()

    # Melt the DataFrame to long format
    melted = pd.melt(grouped_flat, id_vars='t0', value_vars=grouped_flat.columns[1:], var_name='Name Day', value_name='Count')

    # Create the bar plot
    fig = px.bar(melted, x='t0', y='Count', color='Name Day', barmode='stack', text='Count',
                 category_orders={'t0': month_order, 'Name Day': day_order})

    # Update layout
    fig.update_layout(
        title=f'Number of Interventions for "{selected_option}" by Month and Name Day',
        xaxis_title='Month',
        yaxis_title='Number of Interventions'
    )

    return fig


# Define a function to create the heatmap layout
async def bar_chart_1_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()
    
    # Use the first option as the default selected option
    selected_option = 'P002 - Agression - fight - rape'

    # Get the initial figure
    bar_figure = await update_bar_charts(selected_option)
    
    # Define layout for bar chart
    layout = html.Div([
        html.Div([
            dcc.Graph(
                id='bar-chart', 
                figure=bar_figure,
                style={'marginTop': '15px', 'marginLeft': '25px', 'marginRight': '25px'}
            )
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
                value=selected_option,
                style={'width': '80%', 'margin': 'auto'}
            ),
        ], style={'width': '100%', 'padding': '20px 0'}),
        html.P("Conclusions:", style={'font-weight': 'bold', 'margin-top': '20px', 'margin-left': '50px'}),
        html.Ul([
            html.Li('"P002 - Aggression - fight - rape” and “P020 - Intoxication alcohol” interventions mainly take place in June, July and October. Many more interventions take place during the weekends than during the week.'),
            html.Li('"P003 - Cardiac arrest” interventions mainly take place in December.'),
            html.Li('"P010 - Respiratory problems” interventions mainly occur in December and January.'),
            html.Li('"P021 - Intoxication drugs” interventions mainly takes place in October. Once again, many more interventions take place during the weekends than during the week.'),
            html.Li('"P032 - Allergic reactions” interventions mainly occur in July and August. In these two months, more interventions take place during the weekends than during the week.'),
            html.Li('"P036 - Heat stroke - solar stroke” interventions mainly occur in the summer months of June, July and August.'),
            html.Li('"P072 - Sick child < 15 years with fever” interventions mainly occur in December.'),
            html.Li('"P080 - COVID-19” interventions come in waves. The months with the most interventions are July, October and December.')
        ], style={'margin-left': '50px', 'margin-right': '70px', 'text-align': 'justify'})
    ], id='bar-charts-figure')

    return layout
