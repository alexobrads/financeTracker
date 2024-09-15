import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc

from callbacks.income_expenses import update_tab_content, modify_income_table, modify_expenses_table, update_pie_chart, \
    modify_bills_table
from layouts.statistics_tables import monthly_view_table, total_view_table, interest_bar_chart, net_loan_savings, \
    loan_bar_chart

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.CYBORG, 'assets/styles.css'],
                suppress_callback_exceptions=True)

app.callback(
    Output("income-table", "data"),
    Input("add-income-row-button", "n_clicks"),
    Input("income-table", "data"),
    Input("save-income-button", "n_clicks"),
    prevent_initial_call=True
)(modify_income_table)

app.callback(
    Output("expenses-table", "data"),
    Input("add-expense-row-button", "n_clicks"),
    Input("expenses-table", "data"),
    Input("save-expenses-button", "n_clicks"),
    prevent_initial_call=True
)(modify_expenses_table)

app.callback(
    Output("bills-table", "data"),
    Input("add-bill-row-button", "n_clicks"),
    Input("bills-table", "data"),
    Input("save-bills-button", "n_clicks"),
    prevent_initial_call=True
)(modify_bills_table)

app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "active_tab")]
)(update_tab_content)

app.callback(
    Output("pie-chart", "figure"),
    [Input("tabs", "active_tab")]
)(update_pie_chart)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Last Month Summary"),
            dbc.Tabs([
                dbc.Tab(label="Summary", tab_id="summary-tab"),
                dbc.Tab(label="Income", tab_id="income-tab"),
                dbc.Tab(label="Bills", tab_id="bills-tab"),
                dbc.Tab(label="Expenses", tab_id="expenses-tab"),
            ], id="tabs", active_tab="summary-tab"),
            html.Div(id="tabs-content")], width=7),
        dbc.Col([
            dcc.Graph(id='pie-chart')
        ]),
    ], style={'margin-bottom': '50px', 'margin-top': '50px'}),
    dbc.Row([
        dbc.Col([
            html.H3("Total View"),
            total_view_table
        ]),
        dbc.Col([
            html.H3("Monthly View"),
            monthly_view_table
        ]),
    ], style={'margin-bottom': '20px'}),
    dbc.Row([
        dbc.Col([
            html.H3("Interest & Loan Charts"),
            dbc.Tabs([
                dbc.Tab(label="Interest Chart", children=[
                    html.Br(),
                    interest_bar_chart
                ]),
                dbc.Tab(label="Loan Chart", children=[
                    html.Br(),
                    loan_bar_chart
                ]),
            ])
        ], width=6),
        dbc.Col([
            html.H3("Net Loan Savings"),
            net_loan_savings
        ], width=6),
    ]),
])
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
