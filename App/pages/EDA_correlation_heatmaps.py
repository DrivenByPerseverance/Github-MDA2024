import asyncio
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import os

"""
# Define a function to load the dataset asynchronously
async def load_dataset(option):
    if option == 1:
        file_path = '1_Data/CLEANED/subset_correlation_heatmap1.parquet'
        selected_columns = ['eventlevel_trip', 'eventlevel_firstcall']
    elif option == 2:
        file_path = '1_Data/CLEANED/subset_correlation_heatmap2.parquet'
        selected_columns = ['eventtype_trip', 'eventtype_firstcall']
    elif option == 3:
        file_path = '1_Data/CLEANED/subset_correlation_heatmap3.parquet'
        selected_columns = ['eventtype_trip', 'eventlevel_trip']
    elif option == 4:
        file_path = '1_Data/CLEANED/subset_correlation_heatmap4.parquet'
        selected_columns = ['eventlevel_trip', 'vector_type']
    elif option == 5:
        file_path = '1_Data/CLEANED/subset_correlation_heatmap5.parquet'
        selected_columns = ['eventtype_trip', 'vector_type']
    elif option == 6:
        file_path = '1_Data/CLEANED/subset_correlation_heatmap6.parquet'
        selected_columns = ['eventtype_trip', 'abandon_reason']
    else:
        raise ValueError("Invalid option")
    
    # Read the Parquet file into a pandas DataFrame
    interventions_dataset = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return interventions_dataset, selected_columns
"""

# LOAD DATA FROM S3 BUCKET
# Define a function to load the dataset asynchronously with caching
async def load_dataset(option, cache_dir='cache'):
    if option == 1:
        file_path = 's3://mda2024public/CLEANED/subset_correlation_heatmap1.parquet'
        selected_columns = ['eventlevel_trip', 'eventlevel_firstcall']
    elif option == 2:
        file_path = 's3://mda2024public/CLEANED/subset_correlation_heatmap2.parquet'
        selected_columns = ['eventtype_trip', 'eventtype_firstcall']
    elif option == 3:
        file_path = 's3://mda2024public/CLEANED/subset_correlation_heatmap3.parquet'
        selected_columns = ['eventtype_trip', 'eventlevel_trip']
    elif option == 4:
        file_path = 's3://mda2024public/CLEANED/subset_correlation_heatmap4.parquet'
        selected_columns = ['eventlevel_trip', 'vector_type']
    elif option == 5:
        file_path = 's3://mda2024public/CLEANED/subset_correlation_heatmap5.parquet'
        selected_columns = ['eventtype_trip', 'vector_type']
    elif option == 6:
        file_path = 's3://mda2024public/CLEANED/subset_correlation_heatmap6.parquet'
        selected_columns = ['eventtype_trip', 'abandon_reason']
    else:
        raise ValueError("Invalid option")
    
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, f"subset_correlation_heatmap{option}.parquet")
    
    # Check if the file is already cached locally
    if os.path.exists(local_path):
        print(f"Loading subset_correlation_heatmap{option}.parquet from cache")
        interventions_dataset = pd.read_parquet(local_path, engine='pyarrow')
    else:
        # Read the Parquet file into a pandas DataFrame
        print(f"Downloading subset_correlation_heatmap{option}.parquet")
        interventions_dataset = pd.read_parquet(file_path, engine='pyarrow')
        
        # Cache the dataset locally
        interventions_dataset.to_parquet(local_path, engine='pyarrow')
    
    # Simulate data loading time
    await asyncio.sleep(1)
    return interventions_dataset, selected_columns



# Define a function to create the heatmap layout
async def correlation_heatmap_layout():
    # Load the dataset asynchronously
    interventions_dataset, selected_columns = await load_dataset(option=1)  # Default to option 1
    
    # Assuming df_interventions1 is your DataFrame
    df_selected = interventions_dataset[selected_columns]

    # Encoding categorical variables using one-hot encoding
    df_encoded = pd.get_dummies(df_selected)

    # Calculating the correlation matrix
    correlation_matrix = df_encoded.corr()

    # Select the dummy variables of "vector_type" on the y-axis and "eventlevel_trip" on the x-axis
    correlation_subset = correlation_matrix.loc[df_encoded.columns[df_encoded.columns.str.startswith(selected_columns[0])],
                                                df_encoded.columns[df_encoded.columns.str.startswith(selected_columns[1])]]

    # Create a heatmap using Plotly
    heatmap = go.Heatmap(
        z=correlation_subset.values,
        x=correlation_subset.columns,
        y=correlation_subset.index,
        colorscale='RdBu',
        zmin=-1, zmax=1
    )

    # Explanation based on the selected option
    explanations = {
        1: "In the first correlation heatmap the variable 'eventlevel_trip' is compared with 'eventlevel_firstcall'. It can be concluded that the event level is usually correctly determined on the first call.",
        2: "In the second correlation heatmap the variable 'eventtype_trip' is compared with 'eventtype_firstcall'. It can be concluded that the event type is usually correctly determined on the first call.",
        3: "The third correlation heatmap compares the variables 'eventtype_trip' and 'eventlevel_trip'. It can be deduced that 'P003 - Cardiac Arrest' is mainly categorized as event level 'N0' or 'N1', 'P011 - Chest pain', on the other hand, mainly falls under event level 'N2' or 'N3', and 'P004 - Stroke' falls mainly under event level 'N4' or 'N5'.",
        4: "The fourth correlation heatmap compares the variables 'eventlevel_trip' and 'vector_type'. Event levels 'N0' to 'N3' are correlated with the dispatch of a MUG, the event levels 'N3' and 'N4' are correlated with the dispatch of a PIT and the dispatch of an ambulance is strongly correlated with event level 'N5'. The higher the number in the event level, the less dangerous the event. This finding is in line with the fact that an ambulance only transports paramedics, a PIT only transports paramedics and nurses, and a MUG nurses and emergency doctors.",
        5: "The fifth correlation heatmap compares the variables 'eventtype_trip' and 'vector_type'. An ambulance is dispatched in the event of 'P002 - Aggression - fight - rape' or 'P020 - Intoxication alcohol'. An exceptional ambulance is then dispatched for 'P099 - Interhospital transport'. A fire ambulance is dispatched in the event of 'FI (1.3.0) fire building', 'HG (2.1.1) gas odor', 'HG (2.1.2) gas leak', or 'TI (3.3.2) CO intoxication'. Finally, a MUG is issued in the event of 'P003 - Cardiac arrest' or 'P011 - Chest Pain'.",
        6: "The sixth correlation heatmap compares the variables 'eventtype_trip' and 'abandon_reason'. In the case of 'P003 - Cardiac arrest' it may happen that the reason for aborting vector transmission may be that the patient is deceased. In the case of 'P067 - Social problems' it may happen that the reason for aborting vector transmission is that the patient has been taken care of on site."
    }

    return html.Div([  # Return the layout without including the dropdown and graph
        dcc.Graph(
            id='correlation-heatmap', 
            figure=go.Figure(data=[heatmap]), 
            style={'marginLeft': '25px', 'marginRight': '25px'}
        ), 
        dcc.Dropdown(
            id='option-dropdown',
            options=[
                {'label': 'eventlevel_trip vs. eventlevel_firstcall', 'value': 1},
                {'label': 'eventtype_trip vs. eventtype_firstcall', 'value': 2},
                {'label': 'eventtype_trip vs. eventlevel_trip', 'value': 3},
                {'label': 'eventlevel_trip vs. vector_type', 'value': 4},
                {'label': 'eventtype_trip vs. vector_type', 'value': 5},
                {'label': 'eventtype_trip vs. abandon_reason', 'value': 6}
            ],
            value=1,
            style={'width': '80%', 'margin': 'auto'}
        ),
        html.P("Conclusions:", style={'font-weight': 'bold', 'margin-top': '20px', 'margin-left': '50px'}),
        html.Ul([
            html.Li(
                html.Div(
                    id='explanation-heatmaps',
                    children=explanations[1]
                )
            )
        ], style={'margin-left': '50px'})
    ])

# Define callback to update the graph when dropdown value changes
async def update_heatmap(option):
    interventions_dataset, selected_columns = await load_dataset(option)
    df_selected = interventions_dataset[selected_columns]
    df_encoded = pd.get_dummies(df_selected)
    correlation_matrix = df_encoded.corr()
    correlation_subset = correlation_matrix.loc[df_encoded.columns[df_encoded.columns.str.startswith(selected_columns[0])],
                                                df_encoded.columns[df_encoded.columns.str.startswith(selected_columns[1])]]

    heatmap = go.Heatmap(
        z=correlation_subset.values,
        x=correlation_subset.columns,
        y=correlation_subset.index,
        colorscale='RdBu',
        zmin=-1, zmax=1
    )

    return go.Figure(data=[heatmap], layout=go.Layout(
        title=f'Correlation Matrix between {selected_columns[0]} and {selected_columns[1]}',  # Title includes selected columns
        xaxis=dict(title=selected_columns[1]),  # X-axis title
        yaxis=dict(title=selected_columns[0]),  # Y-axis title
        height=400 + 20 * len(correlation_subset.index)  # Adjust height based on number of y-axis labels
    ))


# Define callback to update the explanation text when dropdown value changes
def update_explanation_heatmap(option):
    # Explanation based on the selected option
    explanations = {
        1: "In the first correlation heatmap the variable 'eventlevel_trip' is compared with 'eventlevel_firstcall'. It can be concluded that the event level is usually correctly determined on the first call.",
        2: "In the second correlation heatmap the variable 'eventtype_trip' is compared with 'eventtype_firstcall'. It can be concluded that the event type is usually correctly determined on the first call.",
        3: "The third correlation heatmap compares the variables 'eventtype_trip' and 'eventlevel_trip'. It can be deduced that 'P003 - Cardiac Arrest' is mainly categorized as event level 'N0' or 'N1', 'P011 - Chest pain', on the other hand, mainly falls under event level 'N2' or 'N3', and 'P004 - Stroke' falls mainly under event level 'N4' or 'N5'.",
        4: "The fourth correlation heatmap compares the variables 'eventlevel_trip' and 'vector_type'. Event levels 'N0' to 'N3' are correlated with the dispatch of a MUG, the event levels 'N3' and 'N4' are correlated with the dispatch of a PIT and the dispatch of an ambulance is strongly correlated with event level 'N5'. The higher the number in the event level, the less dangerous the event. This finding is in line with the fact that an ambulance only transports paramedics, a PIT only transports paramedics and nurses, and a MUG nurses and emergency doctors.",
        5: "The fifth correlation heatmap compares the variables 'eventtype_trip' and 'vector_type'. An ambulance is dispatched in the event of 'P002 - Aggression - fight - rape' or 'P020 - Intoxication alcohol'. An exceptional ambulance is then dispatched for 'P099 - Interhospital transport'. A fire ambulance is dispatched in the event of 'FI (1.3.0) fire building', 'HG (2.1.1) gas odor', 'HG (2.1.2) gas leak', or 'TI (3.3.2) CO intoxication'. Finally, a MUG is issued in the event of 'P003 - Cardiac arrest' or 'P011 - Chest Pain'.",
        6: "The sixth correlation heatmap compares the variables 'eventtype_trip' and 'abandon_reason'. In the case of 'P003 - Cardiac arrest' it may happen that the reason for aborting vector transmission may be that the patient is deceased. In the case of 'P067 - Social problems' it may happen that the reason for aborting vector transmission is that the patient has been taken care of on site."
    }
    
    return explanations[option]