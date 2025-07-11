import yfinance as yf
import pandas as pd
import yaml

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def fetch_data(assets, start_date, end_date):
    data = yf.download(assets, start=start_date, end=end_date)['Adj Close']
    data = data.dropna(how='all')
    return data

def preprocess_data(data):
    return data.fillna(method='ffill').fillna(method='bfill')

if __name__ == "__main__":
    config = load_config()
    data = fetch_data(config['assets'], config['start_date'], config['end_date'])
    data = preprocess_data(data)
    print(data.head())
