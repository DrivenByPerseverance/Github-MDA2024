from dash import html
import dash_bootstrap_components as dbc

# Image URL
image_url = 'https://mda2024public.s3.eu-north-1.amazonaws.com/CLEANED/data.png'

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
        # Add the new image
        html.Img(src=image_url, style={'width': '400px', 'display': 'block', 'margin': 'auto'}),
        html.P(
            "This app is developed for the course \"Modern Data Analytics\". It is designed to investigate data from the Citizen Science project 'From Bystander to Hero' in 2024. The original goal of this project was to engage citizens to start cardiopulmonary resuscitation (CPR) in case of cardiac arrest. The data of the project consists of datasets on medical transport, locations of automated external defibrillators (AED) and datasets with interventions. Therefore our first idea was to improve survival rates from cardiac arrests by strategically placing AED devices throughout Belgium, taking into account the proximity of emergency services and the frequency of cardiac arrests. While initially focused on cardiac arrest response optimization, our Dash app offers a platform for broader exploration of data-driven insights which users can explore through interactive visualization and analysis. The app informs citizens and medical professionals about peak times, seasonal variations and any significant patterns in incidents and response times of emergency services. The purpose is to promote a sense of responsibility and preparedness in responding to emergencies, while providing insight to optimize resource allocation and improve patient outcomes.",
            style={'textAlign': 'justify'}  # Justify the paragraph text
        ),
    ], style={'margin': '20px'}),
], className="mt-4")
