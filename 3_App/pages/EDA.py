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

# Define menu for choosing different visualizations
visualization_menu = dbc.Card([
    dbc.CardHeader(html.H4("Choose Visualization")),
    dbc.ListGroup(
        [
            dbc.ListGroupItem("Correlation Heatmaps", href="/correlation_heatmaps"),
            dbc.ListGroupItem("2D Histograms", href="/histograms"),
            dbc.ListGroupItem("Bar charts", href="/bar-charts"),
            dbc.ListGroupItem("Line charts", href="/line-charts"),
            dbc.ListGroupItem("Scatter plots", href="/scatter-plots"),
            dbc.ListGroupItem("Pie charts", href="/pie-charts"),
            dbc.ListGroupItem("Bubble charts", href="/bubble-charts"),
            dbc.ListGroupItem("Maps", href="/maps"),
        ],
        horizontal=True,  # Set the ListGroup to display items horizontally
        className="d-flex justify-content-center flex-wrap",  # Use flexbox to center items horizontally and wrap them to the next line if the horizontal space is insufficient
    ),
], color="light")

exploratory_data_analysis_layout = html.Div([
    html.Div(className="mt-4"),  # Add margin-top for white space
    html.Div([
        header,
        html.Br(),
        visualization_menu,
    ], style={'padding': '0 20px'}),  # Add padding to center the content
    #html.Div("Visualization content will be displayed here...", style={'text-align': 'center'})
])

