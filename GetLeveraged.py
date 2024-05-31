import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def download_data(ticker):
    # Download the historical data
    data = yf.download(ticker, progress=False)
    return data

def preprocess_data(baseline_data, leveraged_data):
    # Calculate daily returns
    baseline_data['Daily Return'] = baseline_data['Adj Close'].pct_change()
    leveraged_data['Daily Return'] = leveraged_data['Adj Close'].pct_change()

    # Align the data by date
    combined_data = pd.DataFrame({
        'Baseline Return': baseline_data['Daily Return'],
        'Leveraged Return': leveraged_data['Daily Return']
    }).dropna()
    
    return combined_data

def train_model(combined_data):
    # Split the data into training and testing sets
    X = combined_data[['Baseline Return']]
    y = combined_data['Leveraged Return']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model

def simulate_leveraged_data(baseline_data, model):
    # Predict leveraged returns using the trained model
    baseline_data['Predicted Leveraged Return'] = model.predict(baseline_data[['Daily Return']].dropna())
    
    # Reconstruct leveraged price data
    baseline_data['Simulated Leveraged Price'] = (1 + baseline_data['Predicted Leveraged Return']).cumprod()
    
    # Normalize the starting price to be the same as the baseline starting price
    baseline_data['Simulated Leveraged Price'] *= baseline_data['Adj Close'].iloc[0]
    
    return baseline_data

if __name__ == "__main__":
    # Prompt user for input and capitalize the tickers
    leveraged_ticker = input("Enter the ticker for the leveraged equity (e.g., TQQQ): ").strip().upper()
    baseline_ticker = input("Enter the ticker for the baseline index (e.g., QQQ): ").strip().upper()
    
    # Download the data
    baseline_data = download_data(baseline_ticker)
    leveraged_data = download_data(leveraged_ticker)
    
    # Preprocess the data
    combined_data = preprocess_data(baseline_data, leveraged_data)
    
    # Train the model
    model = train_model(combined_data)
    
    # Simulate the leveraged data
    simulated_data = simulate_leveraged_data(baseline_data, model)
    
    # Save the simulated data to a CSV file
    simulated_data.to_csv(f'Simulated_{leveraged_ticker}_historical_data.csv')
    
    print(f'Simulated data for {leveraged_ticker} based on {baseline_ticker} saved to CSV file.')
