from dash_table import DataTable
from etl.process_statements import process_offset_statements, process_mortgage_statements, extract_offset_mortgage_statistics
import dash_core_components as dcc
import plotly.graph_objects as go

offset = process_offset_statements()
mortgage = process_mortgage_statements()

monthly_df, total_df = extract_offset_mortgage_statistics(offset, mortgage)

total_view_table = DataTable(
    id='total-view-table',
    columns=[{'name': col, 'id': col} for col in total_df.columns],
    data=total_df.to_dict('records'),
    style_table={'fontSize': '12px', 'backgroundColor': '#343a40', 'color': '#fff', 'border': '1px solid #495057',
                 'overflowX': 'auto', 'overflowY': 'auto'},
    style_cell={'backgroundColor': '#495057', 'color': '#fff'}
)

monthly_view_table = DataTable(
    id='monthly-view-table',
    columns=[{'name': col, 'id': col} for col in monthly_df.columns],
    data=monthly_df.to_dict('records'),
    style_table={'fontSize': '12px', 'backgroundColor': '#343a40', 'color': '#fff', 'border': '1px solid #495057', 'overflowX': 'auto', 'overflowY': 'auto'},
    style_cell={'backgroundColor': '#495057', 'color': '#fff'}
)

# Sample Graph components
interest_bar_chart = dcc.Graph(
    id='interest-bar-chart',
    figure={
        'data': [
            go.Bar(x=monthly_df['Month'], y=monthly_df['Interest Paid'], name='Interest Paid', marker=dict(color='red')),
            go.Bar(x=monthly_df['Month'], y=monthly_df['Interest Saved'], name='Interest Saved', marker=dict(color='green'))
        ],
        'layout': {
            'title': 'Month to Month Interest',
            'barmode': 'group',
            'plot_bgcolor': '#343a40',  # Dark background color for the plot area
            'paper_bgcolor': '#495057',  # Dark background color for the entire graph
            'font': {'color': '#fff'},  # White text color
        }
    }
)

loan_bar_chart = dcc.Graph(
    id='loan-bar-chart',
    figure={
        'data': [
            go.Bar(x=monthly_df['Month'], y=monthly_df['Additional Repayments'], name='Additional Repayments', marker=dict(color='green')),
            go.Bar(x=monthly_df['Month'], y=monthly_df['Principle Paid'], name='Principle Paid', marker=dict(color='red'))
        ],
        'layout': {
            'title': 'Month to Month Principle',
            'barmode': 'group',
            'plot_bgcolor': '#343a40',
            'paper_bgcolor': '#495057',
            'font': {'color': '#fff'},
        }
    }
)

net_loan_savings = dcc.Graph(
    id='net-loan-savings',
    figure={
        'data': [
            go.Bar(x=monthly_df['Month'], y=monthly_df['Loan Balance Change'], name='Loan Balance Change'),
        ],
        'layout': {
            'title': 'Month to Month Savings',
            'barmode': 'stack',
            'plot_bgcolor': '#343a40',
            'paper_bgcolor': '#495057',
            'font': {'color': '#fff'},
        }
    }
)
