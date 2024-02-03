import alpaca_trade_api as tradeapi
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from datetime import timedelta

# Set your Alpaca API key and secret
API_KEY = '#'
API_SECRET = '#'
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading, replace with 'https://api.alpaca.markets' for live trading

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL, api_version='v2')

# Define the stock symbol and time frame
symbol = 'AAPL'
timeframe = '1Min'

# Fetch historical stock data from Alpaca
end_dt = pd.Timestamp.now()
start_dt = end_dt - timedelta(minutes=16)  # Fetch last 15 minutes plus an extra minute for training data

barset = api.get_barset(symbol, timeframe, limit=1000, start=start_dt, end=end_dt)
data = barset[symbol].df

# Feature engineering: Use close prices of the last 15 minutes as features
features = data['close'].iloc[:-1]

# Target variable: The close price of the last minute
target = data['close'].iloc[-1]

# Reshape features to a 2D array (required for scikit-learn)
features = features.values.reshape(-1, 1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Use the trained model to predict the stock price for the next minute
next_minute_features = data['close'].iloc[-15:].values.reshape(1, -1)
predicted_price = model.predict(next_minute_features)

print(f"Predicted Stock Price for the Next Minute: {predicted_price[0]}")
