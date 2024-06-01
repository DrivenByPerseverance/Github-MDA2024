import asyncio
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
from dash import dcc, html
import os

# LOAD DATA FROM FOLDER
"""
# Define a function to load the dataset asynchronously
async def load_dataset():
    file_path = '1_Data/CLEANED/subset_map_subplots.parquet'
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
    filename = 'subset_map_subplots.parquet'
    
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, filename)
    
    # Check if the file is already cached locally
    if os.path.exists(local_path):
        print("Loading subset_map_subplots.parquet from cache")
        subset_selected_events = pd.read_parquet(local_path, engine='pyarrow')
    else:
        # File path to S3 bucket
        file_path = 's3://mda2024public/CLEANED/subset_map_subplots.parquet'
        
        # Read the Parquet file from S3 into a pandas DataFrame
        print("Downloading subset_map_subplots.parquet from S3")
        subset_selected_events = pd.read_parquet(file_path, engine='pyarrow')
        
        # Cache the dataset locally
        subset_selected_events.to_parquet(local_path, engine='pyarrow')
    
    # Simulate data loading time
    await asyncio.sleep(1)
    return subset_selected_events

# Function to generate data and layout for map subplots
def generate_map_layout(subset_selected_events):
    data = []
    layout = dict(
        autosize=True,
        hovermode=False,
        annotations=[]
    )

    subset_selected_events['year_month'] = pd.to_datetime(subset_selected_events['t0']).dt.to_period('M')
    year_months = list(subset_selected_events['year_month'].unique())
    year_months.sort()

    COLS = 6
    ROWS = 2
    z = 0

    for y in reversed(range(ROWS)):
        for x in range(COLS):
            if z >= len(year_months):
                break

            geo_key = 'geo' + str(z + 1) if z != 0 else 'geo'
            subset = subset_selected_events[subset_selected_events['year_month'] == year_months[z]]
            lons = list(subset['longitude_intervention'])
            lats = list(subset['latitude_intervention'])

            if not subset.empty:  # Only add data if there are interventions for this month
                data.append(
                    dict(
                        type='scattergeo',
                        showlegend=False,
                        lon=lons,
                        lat=lats,
                        geo=geo_key,
                        name=str(year_months[z]),
                        marker=dict(
                            size=2,
                            color="rgb(0, 0, 255)",
                            opacity=0.5
                        )
                    )
                )

                layout[geo_key] = dict(
                    scope='europe',
                    center=dict(lon=4.4699, lat=50.5039),
                    showland=True,
                    landcolor='rgb(229, 229, 229)',
                    showcountries=True,
                    countrycolor='rgb(204, 204, 204)',
                    subunitcolor="rgb(255, 255, 255)",
                    showsubunits=True,
                    subunitwidth=2,
                    projection=dict(
                        type='mercator',
                        scale=20
                    ),
                    domain=dict(x=[float(x) / float(COLS), float(x + 1) / float(COLS)], y=[float(y) / float(ROWS), float(y + 1) / float(ROWS)])
                )

                layout['annotations'].append(
                    dict(
                        x=(x + 0.4)*1.065 / COLS,
                        y=(y + 1) / ROWS,  # Adjusting y position for annotation
                        xref='paper',
                        yref='paper',
                        text=str(year_months[z]),
                        showarrow=False,
                        font=dict(size=12, color='black')
                    )
                )

                # Load shapefile
                shapefile_path = 'https://mda2024public.s3.eu-north-1.amazonaws.com/CLEANED/shapefile_BEL_adm2.shp'
                gdf = gpd.read_file(shapefile_path)

                for geom in gdf['geometry']:
                    if geom.geom_type == 'Polygon':
                        x_shape, y_shape = geom.exterior.xy
                        data.append(
                            dict(
                                type='scattergeo',
                                mode='lines',
                                lon=list(x_shape),
                                lat=list(y_shape),
                                line=dict(width=1, color='black'),
                                geo=geo_key,
                                showlegend=False
                            )
                        )
                    elif geom.geom_type == 'MultiPolygon':
                        for polygon in geom.geoms:
                            x_shape, y_shape = polygon.exterior.xy
                            data.append(
                                dict(
                                    type='scattergeo',
                                    mode='lines',
                                    lon=list(x_shape),
                                    lat=list(y_shape),
                                    line=dict(width=1, color='black'),
                                    geo=geo_key,
                                    showlegend=False
                                )
                            )

            z += 1

    layout['height'] = 800
    layout['width'] = 1200
    layout['margin'] = dict(l=20, r=20, t=50, b=50)

    return data, layout


# Function to update the map subplots based on selected option
async def update_map_subplots(selected_option):
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Filter dataset based on the selected option
    filtered_dataset = subset_selected_events[subset_selected_events['eventtype_trip'] == selected_option].copy()

    # Generate data and layout
    data, layout = generate_map_layout(filtered_dataset)

    figure=go.Figure(data=data, layout=layout)

    return figure


# Function to generate map subplot layout
async def map_subplot_layout():
    # Load the dataset asynchronously
    subset_selected_events = await load_dataset()

    # Generate data and layout
    data, layout = generate_map_layout(subset_selected_events)

    layout = html.Div([
        html.H3("Interventions per Year-Month", style={'margin-top': '30px', 'text-align': 'center'}),
        html.Div(
            dcc.Graph(
                id='map-subplots',
                figure=go.Figure(data=data, layout=layout)
            ),
            style={'display': 'flex', 'justify-content': 'center'}
        ),
        html.Div([
            dcc.Dropdown(
                id='option-dropdown',
                options=[
                    {'label': 'P001 - Traffic accident', 'value': 'P001 - Traffic accident'},
                    {'label': 'P032 - Allergic reactions', 'value': 'P032 - Allergic reactions'},
                    {'label': 'P036 - Heat stroke - solar stroke', 'value': 'P036 - Heat stroke - solar stroke'},
                    {'label': 'P072 - Sick child < 15 years with fever', 'value': 'P072 - Sick child < 15 years with fever'},
                    {'label': 'P080 - COVID-19', 'value': 'P080 - COVID-19'}
                ],
                value='P001 - Traffic accident',  # Set default value here
                clearable=False,
                style={'width': '80%', 'margin': 'auto', 'margin-bottom': '40px'}
            ),
        ], style={'width': '100%', 'padding': '10px 0'})
    ], id='map-subplots-figure')

    return layout

