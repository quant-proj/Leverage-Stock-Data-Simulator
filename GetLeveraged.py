import yfinance as yf
import pandas as pd

def download_data(ticker):
    # Download the historical data
    data = yf.download(ticker, progress=False)
    return data

def get_leverage_scalar():
    while True:
        try:
            leverage_scalar = float(input("Enter the scalar for the leveraged equity returns (e.g., 3): "))
            return leverage_scalar
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

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
    baseline_ticker = input("Enter the ticker for the baseline index (e.g., QQQ): ").strip().upper()
    
    # Download the baseline data
    baseline_data = download_data(baseline_ticker)
    
    # Get leverage scalar from the user
    leverage_scalar = get_leverage_scalar()
    
    # Simulate the leveraged ETF data
    simulated_data = simulate_leveraged_data(baseline_data, leverage_scalar)
    
    # Save the simulated data to a CSV file
    output_filename = f'Simulated_{baseline_ticker}_Leveraged_{leverage_scalar}x.csv'
    simulated_data.to_csv(output_filename)
    
    print(f'Simulated leveraged data based on {baseline_ticker} with {leverage_scalar}x leverage saved to {output_filename}.')
