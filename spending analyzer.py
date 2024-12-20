import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import calendar
import os

def load_and_prepare_data(file_paths):
    # Load and combine the data from both CSV files
    dfs = [pd.read_csv(file_path, parse_dates=['Transaction Date']) for file_path in file_paths]
    df = pd.concat(dfs, ignore_index=True)
    
    # Filter only relevant years
    df['Year'] = df['Transaction Date'].dt.year
    df_2023_2024 = df[df['Year'].isin([2023, 2024])]
    
    # Convert 'Amount' column to numeric values
    df_2023_2024['Amount'] = pd.to_numeric(df_2023_2024['Amount'], errors='coerce')
    
    # Filter out positive amounts
    df_2023_2024 = df_2023_2024[df_2023_2024['Amount'] < 0]
    
    return df_2023_2024

def plot_total_spending(df):
    yearly_spending = -df.groupby('Year')['Amount'].sum()
    yearly_spending.plot(kind='bar', color=['blue', 'green'], title='Total Spending 2023 vs 2024')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True, prune='lower', nbins=12))
    plt.ylabel('Total Amount')
    plt.show()

def plot_spending_by_category(df):
    spending_by_category = -df.groupby('Category')['Amount'].sum()
    top_categories = spending_by_category.nlargest(5)
    other_spending = spending_by_category.sum() - top_categories.sum()
    top_categories['Other'] = other_spending
    top_categories.plot(kind='pie', autopct='%1.1f%%', title='Spending by Category (Top 5 + Other)')
    plt.ylabel('')
    plt.show()

def plot_monthly_comparison(df):
    df['Month'] = df['Transaction Date'].dt.month
    monthly_spending = df.groupby(['Month', 'Year'])['Amount'].sum().unstack()
    (-monthly_spending).plot(kind='bar', title='Monthly Spending Comparison 2023 vs 2024', width=0.8)
    plt.ylabel('Amount')
    plt.xlabel('Month')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True, prune='lower', nbins=12))
    plt.xticks(ticks=range(12), labels=[calendar.month_abbr[(i+1)] for i in range(12)], rotation=45)
    plt.show()

def main():
    # file_paths now contain both CSV file paths
    file_paths = [os.path.join('reports', file) for file in os.listdir('reports')]
    
    # Load and combine the data
    df = load_and_prepare_data(file_paths)
    
    # Plot the data
    plot_total_spending(df)
    plot_spending_by_category(df)
    plot_monthly_comparison(df)

if __name__ == "__main__":
    main()
