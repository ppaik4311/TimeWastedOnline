# TimeWastedOnline Project
# Paul Yunsuk Paik
# ppaik4311@gmail.com
# 02/06/2022
# Code for visualizing data on a dashboard format.

from dash import Dash, dash_table
import pandas as pd
from record_parser import yt_records_df as yt_data

app = Dash(__name__)

# Render a summary table showing list of viewed channels and view counts.
app.layout = dash_table.DataTable(
    data=yt_data.to_dict('records'),
    columns=[{'id': column, 'name': column} for column in yt_data.columns],
    style_cell={'textAlign': 'center'},
    style_data={'border':'1px solid black'},
    style_header={'border':'1px solid black'},
)

if __name__ == '__main__':
    app.run_server(debug=True)