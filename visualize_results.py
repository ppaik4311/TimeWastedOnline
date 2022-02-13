# TimeWastedOnline Project
# Paul Yunsuk Paik
# ppaik4311@gmail.com
# 02/06/2022
# Code for visualizing data on a dashboard format.

from dash import dash, Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from record_parser import yt_records_df as yt_data

app = Dash(__name__)

# The first default graph the user will see on the page.
tmp_pareto_default = go.Bar(x=yt_data['channel_name'],
                            y=yt_data['#_of_accessed_time'],
                            name="default_graph"
                     )
layout = go.Layout(#title = "Pareto chart for most viewed Youtube Channels",
                   hovermode='closest'
         )

fig = go.Figure(data=[tmp_pareto_default], 
                layout=layout
      )

# Render a summary table showing li st of viewed channels and view counts.
app.layout = html.Div(children=[
    html.H1('Main driver page',
             style={'fontsize': 14, 
                    'font-family': 'arial black'}
    ),

    html.P('Please select a range to view list of most viewed channel information.',
           style={'fontsize': 12, 
                  'font-family': 'arial'}
    ),
    
    # Block showing output based on user interaction on RangeSlider.
    html.Div(id='ranking_output_block', 
             style={'margin-top': 10,
                    'fontsize': 10,
                    'font-family': 'arial black'}
    ),

    # Interactive range slider to allow user to choose a range of ranks between most viewed channels.
    dcc.RangeSlider(0, yt_data.shape[0],
                    id='channel_ranking_slider',
                    marks={i: f"Rank#{i+1}" for i in range(0, yt_data.shape[0], 500)},
                    step=10,
                    value=[0, 30],
    ),

    # Scatter plot showing data accordingly with user interaction.
    dcc.Graph(
        id='channel_pareto',
        figure=fig
    ),

    # Render an interactive summary table based on range selection.
    html.Div(children=[],
             id='dynamic_summary_table'
    ),
])

# Callback for interactive slider selection range viewer.
@app.callback(
    Output('ranking_output_block', 'children'),
    Input('channel_ranking_slider', 'value')
)
def show_selection_range(input_range):
    """
    Shows user an interactive information regarding selected range.
    """
    return f"MIN bound ranking: {input_range[0]}, MAX bound ranking: {input_range[1]}"

# Callback for dynamic slider - graph interaction.
@app.callback(
    Output('channel_pareto', 'figure'),
    Input('channel_ranking_slider', 'value')
)
def graph_output(input_range):
    """
    Filters data and updates plot based on user selection range.
    """
    min_bound = input_range[0]
    max_bound = input_range[1]
    tmp_pareto_filtered = go.Bar(x=yt_data.iloc[min_bound:max_bound]['channel_name'],
                                 y=yt_data.iloc[min_bound:max_bound]['#_of_accessed_time']
                                )
    fig = go.Figure(data=[tmp_pareto_filtered], 
                    layout=layout
    )
    fig.update_layout(height=1000, 
                      title_text='Pareto chart for most viewed Youtube channels', 
                      title_x=0.5,
                      xaxis_title='Channel_name',
                      yaxis_title='#_of_channel_views',
                      font=dict(
                          family='Courier New, monospace',
                          size=14,
                          color='#151515'
                      )
    )
    return fig

# Callback for dynamic summary table.
@app.callback(
    Output('dynamic_summary_table', 'children'),
    Input('channel_ranking_slider', 'value')
)
def summary_table_output(input_range, top_list_number=5):
    """
    Render a dynamic summary showing top x channel information.
    x is 5 by default.
    """
    min_bound = input_range[0]
    return html.P(
        f'Top-{top_list_number} viewed channels in current selection range.',
        style={'text-indent': 50,
        'font-family': 'arial'}), html.Thead(
        html.Tr([
        html.Th('Channel name'),
        html.Th('# of times viewed')
        ])), html.Tbody([
        html.Tr(
        [html.Td(yt_data['channel_name'][index_value]), 
        html.Td(yt_data['#_of_accessed_time'][index_value])])
        for index_value in range(min_bound, min_bound + top_list_number)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)