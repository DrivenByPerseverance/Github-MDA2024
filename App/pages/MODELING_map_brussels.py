import pandas as pd
import asyncio
from dash import html
import folium
import os

# LOAD DATA FROM FOLDER
"""
# Define a function to load the dataset asynchronously
async def load_dataset():
    # Define the absolute path to the Parquet file
    file_path_emergence_services = '1_Data/CLEANED/hospital_brl.csv'
    file_path_cardiac_events = '1_Data/CLEANED/intervention_aed_brl.csv'
    file_path_old_AED = '1_Data/CLEANED/aed_brl.csv'
    file_path_AED_kmeans = '1_Data/CLEANED/aed_brl_kmeans.csv'
    file_path_AED_lscp ='1_Data/CLEANED/aed_brl_lscp.csv'

    # Read the Parquet file into a pandas DataFrame
    hospital_df = pd.read_csv(file_path_emergence_services)
    cardiac_df = pd.read_csv(file_path_cardiac_events)
    old_aed_df = pd.read_csv(file_path_old_AED)
    aed_kmeans_df = pd.read_csv(file_path_AED_kmeans)
    aed_lscp_df = pd.read_csv(file_path_AED_lscp)

    # Simulate data loading time
    await asyncio.sleep(1)
    return old_aed_df, aed_kmeans_df, aed_lscp_df, hospital_df, cardiac_df
"""

# LOAD DATA FROM S3 BUCKET
# Define a function to load the dataset asynchronously with caching
async def load_dataset(cache_dir='cache'):
    # Define the file paths
    file_path_emergence_services = '1_Data/CLEANED/hospital_brl.csv'
    file_path_cardiac_events = '1_Data/CLEANED/intervention_aed_brl.csv'
    file_path_old_AED = '1_Data/CLEANED/aed_brl.csv'
    file_path_AED_kmeans = '1_Data/CLEANED/aed_brl_kmeans.csv'
    file_path_AED_lscp ='1_Data/CLEANED/aed_brl_lscp.csv'
    
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    
    # Check if the files are already cached locally
    hospital_cache_path = os.path.join(cache_dir, 'hospital_brl.csv')
    cardiac_cache_path = os.path.join(cache_dir, 'intervention_aed_brl.csv')
    old_aed_cache_path = os.path.join(cache_dir, 'aed_brl.csv')
    aed_kmeans_cache_path = os.path.join(cache_dir, 'aed_brl_kmeans.csv')
    aed_lscp_cache_path = os.path.join(cache_dir, 'aed_brl_lscp.csv')
    
    if os.path.exists(hospital_cache_path) and os.path.exists(cardiac_cache_path) \
        and os.path.exists(old_aed_cache_path) and os.path.exists(aed_kmeans_cache_path) \
        and os.path.exists(aed_lscp_cache_path):
        
        print("Loading datasets from cache")
        hospital_df = pd.read_csv(hospital_cache_path)
        cardiac_df = pd.read_csv(cardiac_cache_path)
        old_aed_df = pd.read_csv(old_aed_cache_path)
        aed_kmeans_df = pd.read_csv(aed_kmeans_cache_path)
        aed_lscp_df = pd.read_csv(aed_lscp_cache_path)
        
    else:
        # Read the CSV files into pandas DataFrames
        print("Downloading and caching datasets")
        hospital_df = pd.read_csv(file_path_emergence_services)
        cardiac_df = pd.read_csv(file_path_cardiac_events)
        old_aed_df = pd.read_csv(file_path_old_AED)
        aed_kmeans_df = pd.read_csv(file_path_AED_kmeans)
        aed_lscp_df = pd.read_csv(file_path_AED_lscp)

        # Cache the datasets locally
        hospital_df.to_csv(hospital_cache_path, index=False)
        cardiac_df.to_csv(cardiac_cache_path, index=False)
        old_aed_df.to_csv(old_aed_cache_path, index=False)
        aed_kmeans_df.to_csv(aed_kmeans_cache_path, index=False)
        aed_lscp_df.to_csv(aed_lscp_cache_path, index=False)
    
    # Simulate data loading time
    await asyncio.sleep(1)
    return old_aed_df, aed_kmeans_df, aed_lscp_df, hospital_df, cardiac_df


# Define a function to create the heatmap layout
async def map_brussels_layout():
    # Load the dataset asynchronously
    old_aed_df, aed_kmeans_df, aed_lscp_df, hospital_df, cardiac_df = await load_dataset()

    # Drop rows with NA
    old_aed_df = old_aed_df.dropna(subset=['lat', 'lon'])
    aed_kmeans_df = aed_kmeans_df.dropna(subset=['new_lat', 'new_lon'])
    aed_lscp_df = aed_lscp_df.dropna(subset=['lat', 'lon'])
    hospital_df = hospital_df.dropna(subset=['lat', 'lon'])
    cardiac_df = cardiac_df.dropna(subset=['lat_itv', 'lon_itv'])

    # Create folium map
    belgium_map = folium.Map(location=[50.8476, 4.3572], zoom_start=12)

    # Add circles for emergency services
    hospital_layer = folium.FeatureGroup(name='Emergency Services')
    for idx, row in hospital_df.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=2000,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.4
        ).add_to(hospital_layer)
    hospital_layer.add_to(belgium_map)

    # Add red dots for cardiac events
    cardiac_layer = folium.FeatureGroup(name='Cardiac Events')
    for idx, row in cardiac_df.iterrows():
        folium.Circle(
            location=[row['lat_itv'], row['lon_itv']],
            radius=1,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.4
        ).add_to(cardiac_layer)
    cardiac_layer.add_to(belgium_map)

    # Add circles for AED device locations
    aed_current_layer = folium.FeatureGroup(name='Current AED Locations')
    for idx, row in old_aed_df.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=200,
            color='purple',
            fill=True,
            fill_color='purple',
            fill_opacity=0.4
        ).add_to(aed_current_layer)
    aed_current_layer.add_to(belgium_map)

    # Add circles for AED device locations
    aed_kmeans_layer = folium.FeatureGroup(name='New AED Locations using K-means')
    for idx, row in aed_kmeans_df.iterrows():
        folium.Circle(
            location=[row['new_lat'], row['new_lon']],
            radius=200,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4
        ).add_to(aed_kmeans_layer)
    aed_kmeans_layer.add_to(belgium_map)

    # Add circles for AED device locations
    aed_lscp_layer = folium.FeatureGroup(name='New AED Locations using the Location Set-Covering Problem (LSCP)')
    for idx, row in aed_lscp_df.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=200,
            color='black',
            fill=True,
            fill_color='black',
            fill_opacity=0.4
        ).add_to(aed_lscp_layer)
    aed_lscp_layer.add_to(belgium_map)

    # Add layer control
    folium.LayerControl().add_to(belgium_map)

    # Convert folium map to HTML
    map_html = belgium_map.get_root().render()

    # Define layout for the map with styling
    layout = html.Div(
        [
            html.Div(
                html.P("Locations of:", style={'margin-top': '20px', 'margin-left': '10%', 'text-align': 'left', 'font-weight': 'bold'})
            ),
            html.Div(
                html.Ul(
                    [
                        html.Li("Emergency services (green)"),
                        html.Li("Cardiac events (red)"),
                        html.Li("Current distribution of AED (purple)"),
                        html.Li("New distribution of AED using K-means (blue)"),
                        html.Li("New distribution of AED using the Location Set-Covering Problem (black)")
                    ],
                    style={'list-style-type': 'disc', 'margin-left': '10%', 'text-align': 'left', 'display': 'inline-block'}
                ),
            ),
            html.Div(
                html.Iframe(srcDoc=map_html, width='80%', height='600px'),
                style={'margin': 'auto', 'text-align': 'center', 'padding-top': '15px', 'margin-bottom':'10px'}
            )
        ]
    )

    return layout