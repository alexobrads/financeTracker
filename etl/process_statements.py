import pandas as pd
from glob import glob
from credentials import accountNumber, startDate


def process_offset_statements():
    csv_files = 'data/offset*'
    file_paths = glob(csv_files)
    dfs = []

    for csv_file in file_paths:
        df = pd.read_csv(csv_file)
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)

    header = ['transactionDate', 'processedDate', 'description', 'a', 'credit', 'balance']
    final_df.columns = header

    final_df['transactionDate'] = pd.to_datetime(final_df['transactionDate'], format='%d %b %Y')

    final_df['transactionDate'] = final_df['transactionDate'].dt.strftime('%Y-%m-%d')

    final_df['transactionDate'] = pd.to_datetime(final_df['transactionDate'])

    final_df['month'] = final_df['transactionDate'].dt.to_period('M')

    filtered_df = final_df[final_df['transactionDate'] > f'{startDate}'].reset_index()

    return filtered_df[['transactionDate', 'month', 'description', 'credit', 'balance']].dropna()


def process_mortgage_statements():
    csv_files = 'data/mortgage*'
    file_paths = glob(csv_files)
    dfs = []

    for csv_file in file_paths:
        df = pd.read_csv(csv_file)
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)

    header = ['transactionDate', 'processedDate', 'description', 'a', 'credit', 'balance']
    final_df.columns = header

    final_df['transactionDate'] = pd.to_datetime(final_df['transactionDate'], format='%d %b %Y')

    final_df['transactionDate'] = final_df['transactionDate'].dt.strftime('%Y-%m-%d')

    final_df['transactionDate'] = pd.to_datetime(final_df['transactionDate'])

    final_df['month'] = final_df['transactionDate'].dt.to_period('M')

    filtered_df = final_df[final_df['transactionDate'] > f'{startDate}'].reset_index()

    return filtered_df[['transactionDate', 'month', 'description', 'credit', 'balance']]


def extract_offset_mortgage_statistics(offset, mortgage):
    repayments = mortgage[mortgage['description'].str.contains(f"TFR FROM {accountNumber} TFR", case=False)].groupby(
        'month').agg({'credit': 'sum'}).reset_index()
    interest = mortgage[mortgage['description'].str.contains("Loan Interest", case=False)].groupby('month').agg(
        {'credit': 'sum'}).reset_index()
    mortgage['interest_saved'] = mortgage['description'].str.extract(r'\$([\d,]+\.\d{2})').astype(float)
    interest_saved = mortgage[['month', 'interest_saved']].copy().dropna()

    repayments = repayments.rename(columns={'month': 'month', 'credit': 'repayment'})
    interest = interest.rename(columns={'month': 'month', 'credit': 'interest'})

    offset_last_balance = offset.groupby('month')['balance'].last().reset_index()

    mortgage_last_balance = mortgage.groupby('month')['balance'].last().reset_index()

    result_df = pd.merge(offset_last_balance, mortgage_last_balance, on='month', suffixes=('_offset', '_mortgage'))

    result_df['remaining_loan_balance'] = result_df['balance_offset'] + result_df['balance_mortgage']
    result_df['change_remaining_loan_balance'] = result_df['remaining_loan_balance'].diff()
    result_df = pd.merge(result_df, repayments, on='month', how='inner')
    result_df = pd.merge(result_df, interest, on='month', how='inner')
    result_df = pd.merge(result_df, interest_saved, on='month', how='inner')
    result_df['principle'] = result_df['repayment'] + result_df['interest']

    result_df.balance_mortgage = result_df.balance_mortgage.abs()
    result_df.remaining_loan_balance = result_df.remaining_loan_balance.abs()
    result_df.interest = result_df.interest.abs()
    result_df['additional_principle'] = result_df['change_remaining_loan_balance'] - result_df['repayment']

    result_df = result_df.rename(columns={
        'month': 'Month',
        'balance_offset': 'Offset Balance',
        'balance_mortgage': 'Mortgage Balance',
        'remaining_loan_balance': 'Remaining Loan Balance',
        'change_remaining_loan_balance': 'Loan Balance Change',
        'principle': 'Principle Paid',
        'interest': 'Interest Paid',
        'additional_principle': 'Additional Repayments',
        'interest_saved': 'Interest Saved'
    })

    result_df = result_df[[
        'Month',
        'Mortgage Balance',
        'Offset Balance',
        'Remaining Loan Balance',
        'Loan Balance Change',
        'Principle Paid', 'Interest Paid', 'Additional Repayments', 'Interest Saved']]

    result_df['Month'] = result_df['Month'].dt.strftime('%Y-%m')

    total_interest_paid = result_df[['Interest Paid']].sum().item()
    total_interest_saved = result_df[['Interest Saved']].sum().item()
    total_mortgage = result_df[['Mortgage Balance']].iloc[-1].item()
    total_offset = result_df[['Offset Balance']].iloc[-1].item()
    total_offset_mortgage = result_df[['Remaining Loan Balance']].iloc[-1].item()

    total_df = pd.DataFrame(
        [(total_mortgage, total_offset, total_offset_mortgage, total_interest_saved, total_interest_paid)],
        columns=['Mortgage', 'Offset', 'Remaining Loan Amount', 'Interest Saved', 'Interest Paid'])

    return result_df.round(0)[::-1], total_df.round(0)
