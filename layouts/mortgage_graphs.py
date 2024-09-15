import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from etl.process_statements import process_offset_statements

df1 = process_offset_statements()

scatter_trace = go.Scatter(
    x=df1['transactionDate'],
    y=df1['balance'],
    mode='markers',
    marker=dict(color='black'),
    name='balance'
)

scatter_layout = go.Layout(
    title='',
    xaxis=dict(
        title='',
        showgrid=False,
        tickmode='linear',
        tickangle=45,
        dtick='M1'
    ),
    yaxis=dict(title='')
)


scatter_fig = go.Figure(data=[scatter_trace], layout=scatter_layout)

mortgage_graph = dbc.Col(
        dcc.Graph(
            id='scatter-plot',
            figure=scatter_fig
        )
    )

# file_path2 = 'data/monthly_view.csv'
# df2 = pd.read_csv(file_path2, parse_dates=['date'], date_format='%b %Y')
# df2['month'] = pd.to_datetime(df2['date'], format='%b %Y').dt.month_name()
#
# bar_trace = go.Bar(
#     y=df2['month'],
#     x=df2['diff'],
#     text='$' + df2['diff'].astype(str),
#     marker=dict(color='#5E9141'),
#     orientation='h'
# )
#
# bar_layout = go.Layout(
#     xaxis=dict(title='', showticklabels=False),
#     yaxis=dict(title='', tickvals=df2['month'], ticktext=df2['month'])
# )
#
# bar_fig = go.Figure(data=[bar_trace], layout=bar_layout)
#
# mortgage_bar = dbc.Col(
#         dcc.Graph(
#             id='bar-chart',
#             figure=bar_fig
#         )
#     )
