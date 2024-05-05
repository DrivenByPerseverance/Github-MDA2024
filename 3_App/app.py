import asyncio
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from pages.homepage import homepage_layout
from pages.CLEANING import data_cleaning_layout
#from pages.CLEANING_interventions import cleaning_interventions_layout
from pages.EDA import exploratory_data_analysis_layout
from pages.EDA_histograms import histogram_layout
from pages.EDA_correlation_heatmaps import correlation_heatmap_layout
from pages.EDA_scatter_plots import scatter_plot_layout
from pages.EDA_line_charts import line_chart_layout
from pages.EDA_bar_charts import bar_chart_layout
from pages.EDA_pie_charts import pie_chart_layout
from pages.EDA_bubble_charts import bubble_chart_layout
from pages.EDA_maps import map_layout
from pages.modeling import modeling_layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    elif pathname == '/bar-charts':  # Add route for line plot
        bar_chart = asyncio.run(bar_chart_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(bar_chart)
        ])
    elif pathname == '/line-charts':  # Add route for line plot
        line_plot = asyncio.run(line_chart_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(line_plot)
        ])
    elif pathname == '/scatter-plots':  # Add route for scatter plot
        scatter_plot = asyncio.run(scatter_plot_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(scatter_plot)
        ])
    elif pathname == '/pie-charts':  # Add route for line plot
        pie_chart = asyncio.run(pie_chart_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(pie_chart)
        ])
    elif pathname == '/bubble-charts':  # Add route for line plot
        bubble_chart = asyncio.run(bubble_chart_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(bubble_chart)
        ])
    elif pathname == '/maps':  # Add route for line plot
        map = asyncio.run(map_layout())
        return html.Div([
            exploratory_data_analysis_layout,
            html.Div(map)
        ])
    elif pathname == '/modeling':   # Add route for modeling
        return modeling_layout
    else:
        return '404 Page Not Found'

server = app.server #wsgi.py file

if __name__ == '__main__':
    app.run_server(debug=True)












