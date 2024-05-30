import base64
from dash import html
import dash_bootstrap_components as dbc

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_string

image_path = '3_App/assets/data.png'
base64_encoded_image = image_to_base64(image_path)


# Define homepage layout with theme
homepage_layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Data Cleaning", href="/data-cleaning")),
            dbc.NavItem(dbc.NavLink("Exploratory Data Analysis", href="/exploratory-data-analysis")),
            dbc.NavItem(dbc.NavLink("Modeling", href="/modeling")),
        ],
        brand="Dash app developed by team \"Portugal\" (Charlotte Vercammen and Ye Liu)",
        color="#1984a4",  # Set the color of the navigation bar
        dark=True,
        fluid=True,  # Set the navigation bar to occupy the full width
    ),
    html.Br(),
    html.Div([
        html.H1("Welcome to our Dash app", className="display-4", style={'textAlign': 'center'}),  # Center the heading
        html.Img(src="data:image/png;base64,"+base64_encoded_image, style={'width': '400px', 'display': 'block', 'margin': 'auto'}),  # Add image
        html.P(
            "This app is developed for the course \"Modern Data Analytics\". It is designed to investigate data from the Citizen Science project 'From Bystander to Hero' in 2024. The original goal of this project was to engage citizens to start cardiopulmonary resuscitation (CPR) in case of cardiac arrest. The data of the project consists of datasets on medical transport, locations of automated external defibrillators (AED) and datasets with interventions. Therefore our first idea was to improve survival rates from cardiac arrests by strategically placing AED devices throughout Belgium, taking into account the proximity of emergency services and the frequency of cardiac arrests. While initially focused on cardiac arrest response optimization, our Dash app offers a platform for broader exploration of data-driven insights which users can explore through interactive visualization and analysis. The app informs citizens and medical professionals about peak times, seasonal variations and any significant patterns in incidents and response times of emergency services. The purpose is to promote a sense of responsibility and preparedness in responding to emergencies, while providing insight to optimize resource allocation and improve patient outcomes.",
            style={'textAlign': 'justify'}  # Justify the paragraph text
        ),#html.Img(src="/assets/timestamps.png", style={'width': '400px', 'display': 'block', 'margin': 'auto'}),  # Add image
    ], style={'margin': '20px'}),
], className="mt-4")
