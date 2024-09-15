import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import dash
import plotly.graph_objects as go

app = dash.Dash(__name__)

income_file_path = 'data/income.csv'
bills_file_path = 'data/bills.csv'
expenses_file_path = 'data/expenses.csv'
summary_file_path = 'data/summary.csv'

visible_columns = ['Name', 'Amount', 'Category', 'Frequency']

# Convert 'Frequency' to a consistent unit (e.g., months)
frequency_mapping = {
    'Weekly': 4.33,  # Approximate weeks in a month
    'Fortnightly': 2,  # Twice a month
    'Monthly': 1,
    'Quarterly': 0.33,  # Approximate quarters in a month
    'Yearly': 1 / 12  # Approximate months in a year
}


def create_table(id, df):
    return dash_table.DataTable(
        id=id,
        columns=[
            {'name': col, 'id': col, 'editable': True} if col != 'Frequency' else
            {'name': col, 'id': col, 'editable': True, 'presentation': 'dropdown'} for col in visible_columns
        ],
        data=df.to_dict('records'),
        editable=True,
        dropdown={
            'Frequency': {
                'options': [
                    {'label': "Weekly", 'value': "Weekly"},
                    {'label': "Fortnightly", 'value': "Fortnightly"},
                    {'label': "Monthly", 'value': "Monthly"},
                    {'label': "Quarterly", 'value': "Quarterly"},
                    {'label': "Yearly", 'value': "Yearly"},
                ]
            }
        },
        row_deletable=True,
        style_table={
            'fontSize': '12px',
            'backgroundColor': '#343a40',
            'color': '#fff',
            'border': '1px solid #495057',
            'overflowX': 'auto',
            'overflowY': 'auto',
        },
        style_cell = {
            'backgroundColor': '#495057',
            'color': '#fff',
        },
        style_header = {
            'backgroundColor': 'rgb(40, 40, 40)',
            'fontWeight': 'bold',
        }
    )


def add_row(current_data):
    new_row = {"Name": "", "Amount": None, "Frequency": ""}
    updated_data = current_data + [new_row]
    return updated_data


@app.callback(
    Output("income-table", "data"),
    Input("add-income-row-button", "n_clicks"),
    Input("income-table", "data"),
    Input("save-income-button", "n_clicks"),
    prevent_initial_call=True
)
def modify_income_table(add_row_clicks, current_data, save_data_clicks):
    ctx = dash.callback_context
    if ctx.triggered_id == "add-income-row-button" and add_row_clicks:
        new_table = add_row(current_data)
    else:
        new_table = current_data

    if ctx.triggered_id == "save-income-button" and save_data_clicks:
        pd.DataFrame(new_table, columns=visible_columns).to_csv(income_file_path, index=False, header=True)

    return new_table


@app.callback(
    Output("expenses-table", "data"),
    Input("add-expense-row-button", "n_clicks"),
    Input("expenses-table", "data"),
    Input("save-expenses-button", "n_clicks"),
    prevent_initial_call=True
)
def modify_expenses_table(add_row_clicks, current_data, save_data_clicks):
    ctx = dash.callback_context
    if ctx.triggered_id == "add-expense-row-button" and add_row_clicks:
        new_table = add_row(current_data)
    else:
        new_table = current_data

    if ctx.triggered_id == "save-expenses-button" and save_data_clicks:
        pd.DataFrame(new_table, columns=visible_columns).to_csv(expenses_file_path, index=False, header=True)

    return new_table

@app.callback(
    Output("bills-table", "data"),
    Input("add-bill-row-button", "n_clicks"),
    Input("bills-table", "data"),
    Input("save-bills-button", "n_clicks"),
    prevent_initial_call=True
)
def modify_bills_table(add_row_clicks, current_data, save_data_clicks):
    ctx = dash.callback_context
    if ctx.triggered_id == "add-bill-row-button" and add_row_clicks:
        new_table = add_row(current_data)
    else:
        new_table = current_data

    if ctx.triggered_id == "save-bills-button" and save_data_clicks:
        pd.DataFrame(new_table, columns=visible_columns).to_csv(bills_file_path, index=False, header=True)

    return new_table


def compute_summary():
    # Calculate total income and total expenses per month
    try:
        income_df = pd.read_csv(income_file_path)
    except FileNotFoundError:
        income_df = pd.DataFrame(columns=visible_columns)

    try:
        expenses_df = pd.read_csv(expenses_file_path)
    except FileNotFoundError:
        expenses_df = pd.DataFrame(columns=visible_columns)

    try:
        bills_df = pd.read_csv(bills_file_path)
    except FileNotFoundError:
        bills_df = pd.DataFrame(columns=visible_columns)

    total_income = income_df['Amount'].sum()

    expenses_df['MonthlyAmount'] = expenses_df['Amount'] * expenses_df['Frequency'].map(frequency_mapping)

    total_expenses_per_month = expenses_df['MonthlyAmount'].sum().item()

    bills_df['MonthlyAmount'] = bills_df['Amount'] * bills_df['Frequency'].map(frequency_mapping)

    total_bills_per_month = bills_df['MonthlyAmount'].sum()

    remaining_income = total_income - total_bills_per_month - total_expenses_per_month

    # Create a summary dataframe
    summary_df = pd.DataFrame({
        'Category': ['Total Income', 'Total Bills', 'Total Expenses', 'Remaining Income'],
        'Monthly Amount': [total_income, total_bills_per_month, total_expenses_per_month, remaining_income]
    })

    pd.DataFrame(summary_df, columns=['Category', 'Monthly Amount']).to_csv(summary_file_path, index=False,
                                                                                header=True)

    return summary_df


@app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "active_tab")]
)
def update_tab_content(active_tab):
    if active_tab == "summary-tab":

        updated_summary_df = compute_summary()
        summary_table = dash_table.DataTable(
            id='summary-table',
            columns=[
                {'name': col, 'id': col} for col in ['Category', 'Monthly Amount']
            ],
            data=updated_summary_df.to_dict('records'),
            style_table={
                'fontSize': '12px',
                'backgroundColor': '#343a40',
                'color': '#fff',
                'border': '1px solid #495057',
                'overflowX': 'auto',
                'overflowY': 'auto',
            },
            style_cell = {
                'backgroundColor': '#495057',
                'color': '#fff',
            },
            style_header={
                'backgroundColor': 'rgb(40, 40, 40)',
                'fontWeight': 'bold',
            }
        )

        return [summary_table]

    elif active_tab == "income-tab":
        try:
            income_df = pd.read_csv(income_file_path)
        except FileNotFoundError:
            income_df = pd.DataFrame(columns=visible_columns)

        return [
            create_table("income-table", income_df),
            html.Button('+', id='add-income-row-button', className='mt-3 custom-plus-button'),
            html.Button('Save', id='save-income-button', className='mt-3 custom-save-button')
        ]

    elif active_tab == "expenses-tab":
        try:
            expenses_df = pd.read_csv(expenses_file_path)
        except FileNotFoundError:
            expenses_df = pd.DataFrame(columns=visible_columns)

        return [
            create_table("expenses-table", expenses_df),
            html.Button('+', id='add-expense-row-button', className='mt-3 custom-plus-button'),
            html.Button('Save', id='save-expenses-button', className='mt-3 custom-save-button')
        ]

    elif active_tab == "bills-tab":
        try:
            bills_df = pd.read_csv(bills_file_path)
        except FileNotFoundError:
            bills_df = pd.DataFrame(columns=visible_columns)

        return [
            create_table("bills-table", bills_df),
            html.Button('+', id='add-bill-row-button', className='mt-3 custom-plus-button'),
            html.Button('Save', id='save-bills-button', className='mt-3 custom-save-button')
        ]
    else:
        return html.Div("Invalid Tab")


@app.callback(
    Output("pie-chart", "figure"),
    [Input("tabs", "active_tab")]
)
def update_pie_chart(active_tab):
    if active_tab == "summary-tab":
        try:
            summary_df = pd.read_csv(summary_file_path)
        except FileNotFoundError:
            summary_df = pd.DataFrame(columns=visible_columns)

        pie_chart_figure = {
            'data': [go.Pie(labels=summary_df['Category'].iloc[1:], values=summary_df['Monthly Amount'].iloc[1:])],
            'layout': {
                'title': 'Summary Breakdown',
                'legend': {'x': 1, 'y': 0.5},
                'paper_bgcolor': '#495057',  # Dark background color for the entire graph
                'font': {'color': '#fff'},  # White text color
            },
        }

        return pie_chart_figure

    elif active_tab == "income-tab":
        try:
            income_df = pd.read_csv(income_file_path)
        except FileNotFoundError:
            income_df = pd.DataFrame(columns=visible_columns)

        income_df['MonthlyAmount'] = income_df['Amount'] * income_df['Frequency'].map(frequency_mapping)

        pie_chart_figure = {
            'data': [go.Pie(labels=income_df['Name'], values=income_df['MonthlyAmount'])],
            'layout': {
                'title': 'Income Breakdown',
                'legend': {'x': 1, 'y': 0.5},
                'paper_bgcolor': '#495057',  # Dark background color for the entire graph
                'font': {'color': '#fff'},  # White text color
            },
        }

        return pie_chart_figure

    elif active_tab == "bills-tab":
        try:
            bills_df = pd.read_csv(bills_file_path)
        except FileNotFoundError:
            bills_df = pd.DataFrame(columns=visible_columns)

        bills_df['MonthlyAmount'] = bills_df['Amount'] * bills_df['Frequency'].map(frequency_mapping)

        # Group by category and sum the monthly amounts
        bills_by_category = bills_df.groupby('Category')['MonthlyAmount'].sum()

        pie_chart_figure = {
            'data': [go.Pie(labels=bills_by_category.index, values=bills_by_category)],
            'layout': {
                'title': 'Bills Breakdown',
                'legend': {'x': 1, 'y': 0.5},
                'paper_bgcolor': '#495057',  # Dark background color for the entire graph
                'font': {'color': '#fff'},  # White text color
            },
        }

        return pie_chart_figure

    elif active_tab == "expenses-tab":
        try:
            expenses_df = pd.read_csv(expenses_file_path)
        except FileNotFoundError:
            expenses_df = pd.DataFrame(columns=visible_columns)

        expenses_df['MonthlyAmount'] = expenses_df['Amount'] * expenses_df['Frequency'].map(frequency_mapping)

        # Group by category and sum the monthly amounts
        expenses_by_category = expenses_df.groupby('Category')['MonthlyAmount'].sum()

        pie_chart_figure = {
            'data': [go.Pie(labels=expenses_by_category.index, values=expenses_by_category)],
            'layout': {
                'title': 'Expenses Breakdown',
                'legend': {'x': 1, 'y': 0.5},
                'paper_bgcolor': '#495057',  # Dark background color for the entire graph
                'font': {'color': '#fff'},  # White text color
            },
        }

        return pie_chart_figure
    else:
        # Return an empty figure or None when not on "expenses-tab"
        return {'data': [], 'layout': {}}
