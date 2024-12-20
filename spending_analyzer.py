import pandas as pd
import calendar
import os
from flask import Flask, render_template

app = Flask(__name__)

def load_and_prepare_data(file_paths):
    dfs = [pd.read_csv(file_path, parse_dates=['Transaction Date']) for file_path in file_paths]
    df = pd.concat(dfs, ignore_index=True)
    
    df['Year'] = df['Transaction Date'].dt.year
    df_2023_2024 = df[df['Year'].isin([2023, 2024])]
    
    df_2023_2024['Amount'] = pd.to_numeric(df_2023_2024['Amount'], errors='coerce')
    df_2023_2024 = df_2023_2024[df_2023_2024['Amount'] < 0]
    
    return df_2023_2024

@app.route('/')
def index():
    file_paths = [os.path.join('reports', file) for file in os.listdir('reports')]
    df = load_and_prepare_data(file_paths)
    
    total_spending_data = {
        'labels': df['Year'].unique().tolist(),
        'datasets': [{
            'label': 'Total Spending',
            'data': (-df.groupby('Year')['Amount'].sum()).tolist(),
            'backgroundColor': ['#4e73df', '#1cc88a']  # Consistent colors for 2023 and 2024
        }]
    }
    
    spending_by_category = -df.groupby('Category')['Amount'].sum()
    spending_by_category = spending_by_category[spending_by_category.index != 'Payments and Credits']  # Filter out "Payments & Credits"
    top_categories = spending_by_category.nlargest(5)
    other_spending = spending_by_category.sum() - top_categories.sum()
    spending_by_category_data = {
        'labels': top_categories.index.tolist() + ['Other'],
        'datasets': [{
            'data': top_categories.tolist() + [other_spending],
            'backgroundColor': ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        }]
    }
    
    df['Month'] = df['Transaction Date'].dt.month
    monthly_spending = df.groupby(['Month', 'Year'])['Amount'].sum().unstack()
    monthly_comparison_data = {
        'labels': [calendar.month_abbr[i+1] for i in range(12)],
        'datasets': [{
            'label': str(year),
            'data': (-monthly_spending[year]).tolist(),
            'backgroundColor': color
        } for year, color in zip(monthly_spending.columns, ['#1cc88a', '#4e73df'])]  # Consistent colors for 2023 and 2024
    }
    
    return render_template('index.html', 
                           total_spending_data=total_spending_data, 
                           spending_by_category_data=spending_by_category_data, 
                           monthly_comparison_data=monthly_comparison_data)

if __name__ == "__main__":
    app.run(debug=True)