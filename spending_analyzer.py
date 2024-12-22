import os
import pandas as pd
import calendar
from flask import Flask, render_template
from prophet import Prophet
import matplotlib.pyplot as plt
import mpld3

from long_island_towns import long_island_towns

app = Flask(__name__)

def extract_town(description, town_list):
    for town in town_list:
        if town.lower() in description.lower():
            return town
    return None

def get_lat_lon(town):
    return long_island_towns.get(town, (None, None))

def load_and_prepare_data(file_paths):
    dfs = [pd.read_csv(file_path, parse_dates=['Transaction Date']) for file_path in file_paths]
    df = pd.concat(dfs, ignore_index=True)
    
    df['Year'] = df['Transaction Date'].dt.year
    df_2023_2024 = df[df['Year'].isin([2023, 2024])]
    
    df_2023_2024['Amount'] = pd.to_numeric(df_2023_2024['Amount'], errors='coerce')
    df_2023_2024 = df_2023_2024[df_2023_2024['Amount'] < 0]
    
    df_2023_2024['Town'] = df_2023_2024['Description'].apply(lambda x: extract_town(x, long_island_towns))
    df_2023_2024['Latitude'], df_2023_2024['Longitude'] = zip(*df_2023_2024['Town'].apply(lambda x: get_lat_lon(x) if x else (None, None)))
    
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
    
    grouped_df = df.groupby(['Latitude', 'Longitude']).agg({'Amount': 'sum'}).reset_index()
    location_data = grouped_df[['Latitude', 'Longitude', 'Amount']].dropna().to_dict(orient='records')
    
    return render_template('index.html', 
                           total_spending_data=total_spending_data, 
                           spending_by_category_data=spending_by_category_data, 
                           monthly_comparison_data=monthly_comparison_data,
                           location_data=location_data)

@app.route('/forecast')
def forecast():
    file_paths = [os.path.join('reports', file) for file in os.listdir('reports')]
    df = load_and_prepare_data(file_paths)
    
    df_prophet = df[['Transaction Date', 'Amount']].rename(columns={'Transaction Date': 'ds', 'Amount': 'y'})
    df_prophet['y'] = -df_prophet['y']  # Make amounts positive for forecasting
    
    model = Prophet()
    model.fit(df_prophet)
    
    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    model.plot(forecast, ax=ax)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Spending Amount', fontsize=14)
    ax.legend(['Actual', 'Forecast', 'Uncertainty Interval'], loc='upper left')
    
    forecast_html = mpld3.fig_to_html(fig)
    
    return render_template('forecast.html', forecast_html=forecast_html)

if __name__ == "__main__":
    app.run(debug=True)