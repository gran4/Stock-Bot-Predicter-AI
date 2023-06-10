import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Set the start and end dates for the historical data
start_date = '2020-01-01'
end_date = '2023-06-09'

# Define the stock symbol you want to retrieve data for
stock_symbol = 'AAPL'  # Replace with your desired stock symbol

# Use yfinance to fetch the stock data from Yahoo Finance
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

num_days = 60  # Number of previous days' closing prices to consider

# Preprocess the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))

# Split the data into training and testing sets
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

y_train_size = len(train_data)
days_train = [i for i in range(y_train_size)]
days_test = [i+y_train_size for i in range(y_train_size)]



# Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(num_days, 1)))
model.add(LSTM(50))
model.add(Dense(3))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')


# Train the model
model.fit(np.array(days_train), np.array(train_data), batch_size=32, epochs=20)

# Plot the actual and predicted prices
plt.figure(figsize=(18, 6))

actual_train = plt.plot(days_train, train_data, label='Actual Train')
actual_test = plt.plot(days_test, test_data, label='Actual Test')

plt.title(f'{stock_symbol} Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend([actual_test[0], actual_train[0]], ['Actual Test', 'Actual Train'])
plt.show()