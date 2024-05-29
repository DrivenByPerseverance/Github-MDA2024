from dash import html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

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

# Define the steps of the data cleaning process
steps_1 = [
    "Remove duplicate rows + multiple spacing",
    "Standardize column names (lowercase, spaces replaced by “_”, name changes)",
    "Drop columns",
    "df_interventions_bxl2: convert “eventtype_and_eventlevel” to eventtype_trip + eventlevel_trip",
    "df_cad9: remove Dutch descriptions from eventtype_trip",
    "df_interventions_bxl2 + df_cad9: add English descriptions to “eventtype_trip”",
    "df_interventions_bxl2: standardize “eventlevel_trip” from N0X to NX",
    "Convert timestamps to same format",
    "df_cad9: delete data before June 1, 2022",
    "Function to find minimum timestamps to remove for consecutive timestamps",
    "Add t0_Hour, t0_Day, t0_Month, t0_DayName columns",
    "Convert “longitude” and “latitude” to fall within the range of Belgium",
    "Delete rows with 'NLD', 'DEU', 'FRA' or 'LUX' in “cityname_intervention”",
    "Merge datasets",
    "Remove non-numeric characters from “house number” and “postal code”",
    "In \"vector_type\", replace 'AMB' with 'Ambulance'",
    "Replace Dutch values from “vector_type” + “abandon_reason” with English translations",
    "Replace 'None' with 'NaN'",
    "Create subsets"
]

# Define the nodes and edges for the cytoscape layout
nodes_1 = [{'data': {'id': f'step-{i}', 'label': step}} for i, step in enumerate(steps_1)]
edges_1 = [{'data': {'source': f'step-{i}', 'target': f'step-{i+1}'}} for i in range(len(steps_1) - 1)]

# Create the layout using cytoscape
cytoscape_layout_1 = cyto.Cytoscape(
    id='timeline',
    layout={'name': 'breadthfirst', 'roots': '[id = "step-0"]'},
    style={'width': '100%', 'height': '800px'},
    elements=nodes_1 + edges_1
)

# Define the steps of the data cleaning process
steps_2 = [
    "Standardize columns with string type by removing spacing next to '-' and capitalizing",
    "Convert “postcode“ from float to string → join with \"address\", \"province\" and \"municipality\" to produce the full address",
    "PIT: extract the hospital name and campus name from “campus”",
    "Get the latitude and longitude using GoogleMap API (a key is needed)",
    "AED + interventions data sets: Get the provinces using the polygon shape in \"Belgium.provinces.WGS84.geojson\"",
    "Calculate the distance between each intervention and the nearest AED / hospital"
]

# Define the nodes and edges for the cytoscape layout
nodes_2 = [{'data': {'id': f'step-{i}', 'label': step}} for i, step in enumerate(steps_2)]
edges_2 = [{'data': {'source': f'step-{i}', 'target': f'step-{i+1}'}} for i in range(len(steps_2) - 1)]

# Create the layout using cytoscape
cytoscape_layout_2 = cyto.Cytoscape(
    id='timeline',
    layout={'name': 'breadthfirst', 'roots': '[id = "step-0"]'},
    style={'width': '100%', 'height': '800px'},
    elements=nodes_2 + edges_2
)


# Create the layout
data_cleaning_layout = html.Div([
    html.Div(className="mt-4"),  # Add margin-top for white space
    html.Div([
        header,
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H3("Data cleaning of the interventions data sets", style={'textAlign': 'center'}),
                cytoscape_layout_1
            ], width=6),  # First column takes up 6 out of 12 columns
            dbc.Col([
                html.H3("Data cleaning of the locations data sets", style={'textAlign': 'center'}),
                html.H3("(AED devices, Ambulance, PIT, MUG)", style={'textAlign': 'center'}),
                cytoscape_layout_2
            ], width=6),  # Second column takes up 6 out of 12 columns
        ], className="mt-3")  # Add margin-top to the row
    ], style={'padding': '0 20px'}),  # Add padding to center the content
])
