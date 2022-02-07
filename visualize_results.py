# TimeWastedOnline Project
# Paul Yunsuk Paik
# ppaik4311@gmail.com
# 02/06/2022
# Code for visualizing data on a dashboard format.

from dash import Dash, dash_table, dcc, html
import plotly.express as px
import pandas as pd
from record_parser import yt_records_df as yt_data

app = Dash(__name__)
fig = px.bar(yt_data, x="channel_name", y="#_of_accessed_time", 
             width=2000, height=1000)

# Render a summary table showing list of viewed channels and view counts.
app.layout = html.Div(children=[
    html.H1(children='This is just a test to see how much I waste my life online'),
    dcc.Graph(
        id='test-graph',
        figure=fig,
    ),
    dash_table.DataTable(
    data=yt_data.to_dict('records'),
    columns=[{'id': column, 'name': column} for column in yt_data.columns],
    style_cell={'textAlign': 'center'},
    style_data_conditional=[
        {
        'if': {'column_id': '#_of_accessed_time'},
        'backgroundColor': '#A9F5F2',
    }],
    style_data={'border':'1px solid black',},
    style_header={'border':'1px solid black'},
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)