from dash import html
import dash_bootstrap_components as dbc

# Define homepage layout with theme
homepage_layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Data Cleaning", href="/data-cleaning")),
            dbc.NavItem(dbc.NavLink("Exploratory Data Analysis", href="/exploratory-data-analysis")),
            dbc.NavItem(dbc.NavLink("Modeling", href="/modeling")),
        ],
        brand="Dash app for the project of the course \"Modern Data Analytics\"",
        color="#1984a4",  # Set the color of the navigation bar
        dark=True,
        fluid=True,  # Set the Navbar to occupy the full width
    ),
    html.Br(),
    html.Div([
        html.H1("Welcome to our Dash app", className="display-4"),
        html.Img(src="/assets/data.png", style={'width': '400px', 'display': 'block', 'margin': 'auto'}),  # Add image
        html.P("This app is developed by team \"Portugal\" (Charlotte Vercammen and Ye Liu) for the project of the course \"Modern Data Analytics\". It is designed to investigate data from the Citizen Science project 'From Bystander to Hero' in 2024. The data consists of datasets on medical transport, locations of Automated External Defibrillators (AED) and datasets with interventions. The original goal of this project was to engage citizens to start Cardiopulmonary resuscitation (CPR) in case of cardiac arrest. Therefore our first idea was to improve survival rates from cardiac arrests by strategically placing AED devices throughout Belgium, taking into account the proximity of emergency services and the frequency of cardiac arrests. While initially focused on cardiac arrest response optimization, our Dash app offers a platform for broader exploration of data-driven insights which users can explore through interactive visualization and analysis. The app informs citizens and medical professionals about peak times, seasonal variations and any significant patterns in incidents and response times of emergency services. The purpose is to promote a sense of responsibility and preparedness in responding to emergencies, while providing insight to optimize resource allocation and improve patient outcomes."),
        html.Img(src="/assets/timestamps.png", style={'width': '400px', 'display': 'block', 'margin': 'auto'}),  # Add image
    ], style={'textAlign': 'center', 'margin': '20px'}),
], className="mt-4")
