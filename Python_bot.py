import alpaca_trade_api as tradeapi
import pandas as pd

# Set your Alpaca API key and secret
API_KEY = 'api_key'
API_SECRET = 'api_secret'
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading, replace with 'https://api.alpaca.markets' for live trading

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL, api_version='v2')

# Define the stock symbol and time frame
symbol = 'AAPL'
timeframe = '15Min'

# Define moving average parameters
short_window = 40
long_window = 100

# Function to get historical data from Alpaca
def get_historical_data(symbol, timeframe, limit=200):
    historical_data = api.get_bars(symbol, timeframe, limit=limit)
    return historical_data

# Function to calculate moving averages
def calculate_moving_averages(data, short_window, long_window):
    data['Short_MA'] = data['close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['close'].rolling(window=long_window, min_periods=1).mean()
    return data

# Function to execute trading strategy
def execute_trading_strategy(data):
    signal = 0  # 1 for Buy, -1 for Sell, 0 for Hold
    if data['Short_MA'].iloc[-1] > data['Long_MA'].iloc[-1] and data['Short_MA'].iloc[-2] <= data['Long_MA'].iloc[-2]:
        signal = 1  # Buy signal
    elif data['Short_MA'].iloc[-1] < data['Long_MA'].iloc[-1] and data['Short_MA'].iloc[-2] >= data['Long_MA'].iloc[-2]:
        signal = -1  # Sell signal
    return signal

# Main function to run the trading bot
def run_trading_bot():
    historical_data = get_historical_data(symbol, timeframe)
    historical_data = calculate_moving_averages(historical_data, short_window, long_window)
    signal = execute_trading_strategy(historical_data)

    # Implement your order execution logic based on the signal
    if signal == 1:
        # Execute buy order
        print('Executing Buy Order')
    elif signal == -1:
        # Execute sell order
        print('Executing Sell Order')
    else:
        # No action
        print('Holding Position')

if __name__ == "__main__":
    run_trading_bot()
