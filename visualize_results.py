# TimeWastedOnline Project
# Paul Yunsuk Paik
# ppaik4311@gmail.com
# 02/06/2022
# Code for visualizing data on a dashboard format.

from dash import Dash, html
import pandas as pd
from record_parser import yt_records_df as yt_data

def generate_table(input_df, max_rows=10):
    """
    Generate a summary table.
    """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in input_df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(input_df.iloc[i][col]) for col in input_df.columns
            ]) for i in range(min(len(input_df), max_rows))
        ])
    ])


app = Dash(__name__)

app.layout = html.Div([
    html.H4(children='My Youtube view history summary'),
    generate_table(yt_data)
])

if __name__ == '__main__':
    app.run_server(debug=True)