from dash import html
import dash_bootstrap_components as dbc

# Define header with the same style as the homepage
header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Data Cleaning", href="/data-cleaning")),
        dbc.NavItem(dbc.NavLink("Exploratory Data Analysis", href="/exploratory-data-analysis")),
        dbc.NavItem(dbc.NavLink("Modeling", href="/modeling")),
    ],
    brand="Homepage",
    brand_href="/",
    color="#1984a4",  # Set the color of the navigation bar
    dark=True,
    fluid=True,
)

# Define menu for choosing different modeling
modeling_menu = dbc.Card([
    dbc.CardHeader(html.H4("Choose Map")),
    dbc.ListGroup(
        [
            dbc.ListGroupItem("Belgium", href="/map-belgium"),
            dbc.ListGroupItem("Brussels", href="map-brussels"),
        ],
        horizontal=True,  # Set the ListGroup to display items horizontally
        className="d-flex justify-content-center flex-wrap",  # Use flexbox to center items horizontally and wrap them to the next line if the horizontal space is insufficient
    ),
], color="light")

modeling_layout = html.Div([
    html.Div(className="mt-4"),  # Add margin-top for white space
    html.Div([
        header,
        html.Br(),
        modeling_menu,
    ], style={'padding': '0 20px'}),  # Add padding to center the content
])

