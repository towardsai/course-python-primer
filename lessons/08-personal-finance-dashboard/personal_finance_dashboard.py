# ==========================
# Personal Finance Dashboard (Single-Snippet Version)
# ==========================

import pandas as pd
import plotly.express as px
from datetime import datetime
import os

CSV_FILENAME = "finance_data.csv"

def write_transaction_to_file(date_str, amount, category, transaction_type):
    with open(CSV_FILENAME, mode="a", encoding="utf-8") as file:
        if os.stat(CSV_FILENAME).st_size == 0:
            file.write("Date,Amount,Category,Type\n")
        file.write(f"{date_str},{amount},{category},{transaction_type}\n")

def read_transactions_from_file():
    if not os.path.exists(CSV_FILENAME):
        return pd.DataFrame(columns=["Date", "Amount", "Category", "Type"])
    df = pd.read_csv(CSV_FILENAME)
    return df

def input_transaction():
    date_str = input("Enter the date (YYYY-MM-DD) or 'done' to stop: ")
    if date_str.lower() == "done":
        return None

    amount_str = input("Enter the amount (positive number): ")
    category = input("Enter the category of this transaction (e.g. Rent, Groceries): ")
    transaction_type = input("Is this an 'income' or 'expense'? ")

    try:
        amount_val = float(amount_str)
    except ValueError:
        print("Invalid amount. Please try again.")
        return {}

    write_transaction_to_file(date_str, amount_val, category, transaction_type)
    print("Transaction saved!")
    return {}

def show_charts():
    df = read_transactions_from_file()
    if df.empty:
        print("No data available to show charts!")
        return

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")

    # Prompt user for date range
    start_date_str = input("Enter start date (YYYY-MM-DD) or leave blank for min: ")
    end_date_str = input("Enter end date (YYYY-MM-DD) or leave blank for max: ")

    try:
        if start_date_str.strip():
            start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
            df = df[df["Date"] >= start_dt]
        if end_date_str.strip():
            end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
            df = df[df["Date"] <= end_dt]
    except ValueError:
        print("Invalid date format, showing all data instead.")

    if df.empty:
        print("No data in this date range.")
        return

    # Bar chart: total income vs total expenses
    df_type = df.groupby("Type")["Amount"].sum().reset_index()
    fig_bar_type = px.bar(df_type, x="Type", y="Amount", title="Total Income vs. Total Expenses", width=800, height=400)
    fig_bar_type.show()

    # Monthly trend line chart
    df["Month"] = df["Date"].dt.to_period("M")
    monthly_df = df.groupby("Month")["Amount"].sum().reset_index()
    monthly_df["MonthStart"] = monthly_df["Month"].dt.to_timestamp()
    fig_line = px.line(monthly_df, x="MonthStart", y="Amount", title="Monthly Total (Income + Expenses)")
    fig_line.show()

    # Pie chart: distribution by category
    df_grouped = df.groupby("Category")["Amount"].sum().reset_index()
    fig_pie_cat = px.pie(df_grouped, names="Category", values="Amount", title="Distribution by Category", width=800, height=400)
    fig_pie_cat.show()

def main():
    print("=== Personal Finance Dashboard ===")
    while True:
        result = input_transaction()
        if result is None:
            break
    show_charts()

if __name__ == "__main__":
    main()
