import sys
import os
import asyncio
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from App.pages.homepage import homepage_layout
from App.pages.CLEANING import data_cleaning_layout
from App.pages.EDA import exploratory_data_analysis_layout
from App.pages.EDA_correlation_heatmaps import correlation_heatmap_layout, update_heatmap, update_explanation_heatmap
from App.pages.EDA_histograms import histogram_layout, update_histograms
from App.pages.EDA_line_charts_1 import line_chart_1_layout
from App.pages.EDA_line_charts_2 import line_chart_2_layout
from App.pages.EDA_bar_charts_1 import bar_chart_1_layout, update_bar_charts
from App.pages.EDA_bar_charts_2 import bar_chart_2_layout
from App.pages.EDA_pie_charts import pie_charts_layout, update_pie_charts
from App.pages.EDA_map_subplots import map_subplot_layout, update_map_subplots
from App.pages.EDA_bubble_map import bubble_map_layout, update_bubble_map
from App.pages.MODELING import modeling_layout
from App.pages.MODELING_map_belgium import map_belgium_layout
from App.pages.MODELING_map_brussels import map_brussels_layout


# External CSS
external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
    dbc.themes.BOOTSTRAP,
    {
        "href": "styles.css",
        "rel": "stylesheet"
    }
]

app = dash.Dash(__name__, external_stylesheets=external_css, suppress_callback_exceptions=True)

# Needed for deployment
application = app.server 

# Lay-out
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return homepage_layout
    elif pathname == '/data-cleaning':  # Add route for data cleaning
        return data_cleaning_layout
    elif pathname == '/exploratory-data-analysis':
        return exploratory_data_analysis_layout
    elif pathname == '/correlation_heatmaps':  # Add route for line plot
        heatmap = asyncio.run(correlation_heatmap_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(heatmap)
        ])
    elif pathname == '/histograms':  # Add route for line plot
        histograms = asyncio.run(histogram_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(histograms)
        ])
    elif pathname == '/line-charts-1':  # Add route for scatter plot
        line_chart1 = asyncio.run(line_chart_1_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(line_chart1)
        ])
    elif pathname == '/line-charts-2':  # Add route for line plot
        line_chart2 = asyncio.run(line_chart_2_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(line_chart2)
        ])
    elif pathname == '/bar-charts-1':  # Add route for line plot
        bar_chart1 = asyncio.run(bar_chart_1_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(bar_chart1)
        ])
    elif pathname == '/bar-charts-2':  # Add route for line plot
        bar_chart2 = asyncio.run(bar_chart_2_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(bar_chart2)
        ])
    elif pathname == '/pie-charts':  # Add route for line plot
        pie_chart = asyncio.run(pie_charts_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(pie_chart)
        ])
    elif pathname == '/map-subplots':  # Add route for map subplots
        map_subplots = asyncio.run(map_subplot_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(map_subplots)
        ])
    elif pathname == '/bubble-map':  # Add route for line plot
        bubble_chart = asyncio.run(bubble_map_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(bubble_chart)
        ])
    elif pathname == '/modeling':   # Add route for modeling
        return modeling_layout
    elif pathname == '/map-belgium':  # Add route for line plot
        map_belgium = asyncio.run(map_belgium_layout())
        return html.Div([
            modeling_layout,
            html.Div(map_belgium)
        ])
    elif pathname == '/map-brussels':  # Add route for line plot
        map_brussels = asyncio.run(map_brussels_layout())
        return html.Div([
            modeling_layout,
            html.Div(map_brussels)
        ])
    else:
        return '404 Page Not Found'


# Define the callback to update the correlation heatmaps figure based on the selected option
@app.callback(Output('correlation-heatmap', 'figure'),
              [Input('option-dropdown', 'value')])
def update_heatmap_figure(value):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(update_heatmap(value))

@app.callback(
    Output('explanation-heatmaps', 'children'),
    [Input('option-dropdown', 'value')]
)
def update_explanation_callback(value):
    return update_explanation_heatmap(value)

# Define the callback to update the histograms based on the selected option
@app.callback(
    [Output('histogram-year', 'figure'),
     Output('histogram-week', 'figure')],
    [Input('option-dropdown', 'value')]
)
def update_histogram_figure(value):
    histogram_figure = asyncio.run(update_histograms(value))
    return histogram_figure

# Call back functions pie charts + text
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('option-dropdown', 'value')]
)
def update_pie_chart_figure(value):
    pie_chart_figure = asyncio.run(update_pie_charts(value))
    return pie_chart_figure

# Define the callback to update the bar chart figure based on the selected option
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('option-dropdown', 'value')]
)
def update_bar_chart_figure(selected_option):
    # Call the update_bar_charts function asynchronously to get the updated figure
    bar_chart_figure = asyncio.run(update_bar_charts(selected_option))
    return bar_chart_figure


# Define callback to update the figure based on the dropdown selection
@app.callback(
    Output('map-subplots', 'figure'),
    Input('option-dropdown', 'value')
)
def update_map_subplots_figure(selected_option):
    # Call the function to update the map subplot layout asynchronously
    map_subplots_layout = asyncio.run(update_map_subplots(selected_option))
    return map_subplots_layout

# Define callback to update the figure based on date range selection
@app.callback(
    Output('bubble-map', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_bubble_map_figure(start_date, end_date):
    # Call the function to update the map subplot layout asynchronously
    bubble_map_layout = asyncio.run(update_bubble_map(start_date, end_date))
    return bubble_map_layout

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=80, debug=True) # Host + port needs to be the same as in Procfile




