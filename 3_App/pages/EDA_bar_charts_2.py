import base64
import os
import asyncio
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_string

image_path = '3_App/assets/timestamps.png'
base64_encoded_image = image_to_base64(image_path)


# Define a function to load the dataset asynchronously
async def load_dataset(filename):
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the Parquet file
    file_path = os.path.join(script_dir, '../data', filename)
    # Normalize the path
    file_path = os.path.normpath(file_path)
    # Read the Parquet file into a pandas DataFrame
    dataset = pd.read_parquet(file_path, engine='pyarrow')
    # Simulate data loading time
    await asyncio.sleep(1)
    return dataset

# Define a function to create a bar chart figure
def create_bar_chart_figure(dataset, title):
    # Convert columns t0, t1, t2, t3, t4, t5, t6, t7 to datetime format with UTC timezone awareness
    for col in ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']:
        dataset[col] = pd.to_datetime(dataset[col], utc=True)

    # Calculate the time differences in minutes
    dataset['T0 -> T1'] = (dataset['t1'] - dataset['t0']).dt.total_seconds() / 60
    dataset['T1 -> T2'] = (dataset['t2'] - dataset['t1']).dt.total_seconds() / 60
    dataset['T2 -> T3'] = (dataset['t3'] - dataset['t2']).dt.total_seconds() / 60
    dataset['T3 -> T4'] = (dataset['t4'] - dataset['t3']).dt.total_seconds() / 60
    dataset['T4 -> T5'] = (dataset['t5'] - dataset['t4']).dt.total_seconds() / 60
    dataset['T5 -> T6'] = (dataset['t6'] - dataset['t5']).dt.total_seconds() / 60
    dataset['T6 -> T7'] = (dataset['t7'] - dataset['t6']).dt.total_seconds() / 60

    # Group by vector type and calculate the mean time differences for each group
    grouped = dataset.groupby('vector_type').median(numeric_only=True)

    # Create traces for each vector type
    data = []
    for vector_type, row in grouped.iterrows():
        trace = go.Bar(x=['T0 -> T1', 'T1 -> T2', 'T2 -> T3', 'T3 -> T4', 'T4 -> T5', 'T5 -> T6', 'T6 -> T7'],
                       y=row[['T0 -> T1', 'T1 -> T2', 'T2 -> T3', 'T3 -> T4', 'T4 -> T5', 'T5 -> T6', 'T6 -> T7']],
                       name=vector_type)
        data.append(trace)

    # Create layout
    layout = go.Layout(title=title,
                       xaxis=dict(title='t Columns'),
                       yaxis=dict(title='Median Time Difference (minutes)'),
                       barmode='group',  # Add barmode to group bars
                       legend=dict(title='Vector Type'))

    # Create figure
    fig = go.Figure(data=data, layout=layout)
    return fig

# Define a function to create the bar chart layout
async def bar_chart_2_layout():
    # Load the main dataset asynchronously
    interventions_dataset = await load_dataset('interventions_dataset.parquet')
    fig1 = create_bar_chart_figure(interventions_dataset, 'Median Time Differences by Step in the Process and Vector Type (All interventions)')

    # Load the subset cardiac dataset asynchronously
    subset_cardiac_dataset = await load_dataset('subset_cardiac.parquet')
    fig2 = create_bar_chart_figure(subset_cardiac_dataset, 'Median Time Differences by Step in the Process and Vector Type (P003 - Cardiac Arrest)')

    # Define layout for the bar charts
    bar_chart_layout = html.Div([
        html.Div([
            html.P("Steps in the process:", style={'margin-top': '20px', 'text-align': 'center', 'font-weight': 'bold'}),
            html.Img(src="data:image/png;base64,"+base64_encoded_image, style={'width': '400px', 'display': 'block', 'margin': 'auto', 'margin-bottom': '20px'}),
        ]),
        html.Div([
            dcc.Graph(
                figure=fig1,
                style={'marginLeft': '25px', 'marginRight': '25px'}
            ),
            html.P("Conclusions:", style={'font-weight': 'bold', 'margin-left': '50px'}),
            html.Ul([
                html.Li('In the case of the vector type "decontamination ambulance", on the one hand the step between "call answered by operator (T0)" and "vector alarmed by operator (T1)" is much slower than with other vector types and on the other hand the step between "vector alarmed by operator (T1)" and "vector leaves to intervention location (T2)".'),
                html.Li('In the case of the vector types "fire ambulance" and "MUG", the step between "vector arrives at intervention location (T3)" and "vector leaves to destination hospital (T4)" is slower than with other vector types.'),
                html.Li('In the case of the vector types "MUG Event", the step between "vector leaves to destination hospital (T4)" and "vector arrives at the destination hospital (T5)" is slower than with other vector types.'),
                html.Li('In the case of the vector type "ambulance exceptional", on the one hand the step between "vector arrives at the destination hospital (T5)" and "vector leaves at the destination hospital (T6)" is much slower than with other vector types and on the other hand the step between "vector leaves at the destination hospital (T6)" and "vector available again (T7)".'),
                html.Li('In the case of vector type "ambulance", all steps except the step between "vector arrives at the destination hospital (T5)" and "vector leaves at the destination hospital (T6)" are faster compared to MUG and PIT vector types.'),
            ], style={'margin-left': '50px', 'margin-right': '70px', 'text-align': 'justify'})
        ]),
        html.Div([
            dcc.Graph(
                figure=fig2,
                style={'marginLeft': '25px', 'marginRight': '25px'}
            ),
            html.P("Conclusions:", style={'font-weight': 'bold', 'margin-left': '50px'}),
            html.Ul([
                html.Li('In the case of "P003 - Cardiac Arrest" event types with vector type "fire ambulance", the following steps are slower than with other vector types: the step between "call answered by operator (T0)" and "vector alarmed by operator (T1)", the step between "vector alarmed by operator (T1)" and "vector leaves to intervention location (T2)", and the step between "vector leaves to intervention location (T2)" and "vector arrives at intervention location (T3)".'),
                html.Li('In the case of "P003 - Cardiac Arrest" event types with vector type "ambulance event", the step between "vector arrives at the destination hospital (T5)" and "vector leaves at the destination hospital (T6)" is slower than with other vector types.')
            ], style={'margin-left': '50px', 'margin-right': '70px', 'text-align': 'justify'})
        ])
    ])

    return bar_chart_layout

