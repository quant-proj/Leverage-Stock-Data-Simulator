import yfinance as yf
import pandas as pd

##### Hardcoded user inputs
usr_ticker = 'QQQ'   # Hardcode the un-leveraged ticker in quotes 
usr_scalar = 3  # Hardcode the scalar that maps the daily returns between the un-leveraged to leveraged equity 

def download_data(ticker):
    # Download the historical data
    data = yf.download(ticker, progress=False)
    return data

def simulate_leveraged_data(baseline_data, leverage_scalar):
    # Calculate daily returns
    baseline_data['Daily Return'] = baseline_data['Adj Close'].pct_change()

    # Simulate leveraged returns
    baseline_data['Leveraged Return'] = baseline_data['Daily Return'] * leverage_scalar

    # Reconstruct leveraged price data
    baseline_data['Simulated Leveraged Price'] = (1 + baseline_data['Leveraged Return']).cumprod()
    
    # Normalize the starting price to match the baseline's starting price
    baseline_data['Simulated Leveraged Price'] *= baseline_data['Adj Close'].iloc[0]

    return baseline_data

if __name__ == "__main__":
    # Prompt user for input and capitalize the tickers
    baseline_ticker = usr_ticker
    
    # Download the baseline data
    baseline_data = download_data(baseline_ticker)
    
    # Get leverage scalar from the user
    leverage_scalar = usr_scalar
    
    # Simulate the leveraged ETF data
    simulated_data = simulate_leveraged_data(baseline_data, leverage_scalar)
    
    # Save the simulated data to a CSV file
    output_filename = f'Simulated_{baseline_ticker}_Leveraged_{leverage_scalar}x.csv'
    simulated_data.to_csv(output_filename)
    
    print(f'Simulated leveraged data based on {baseline_ticker} with {leverage_scalar}x leverage saved to {output_filename}.')
