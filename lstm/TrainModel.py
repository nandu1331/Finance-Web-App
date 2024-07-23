import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping
import datetime as dt

print("getting data")

# Define stock symbol and date range
symbol = 'RELIANCE.NS'
start = '2011-06-21'
end = '2024-07-21'

# Fetch historical data
ds = yf.download(symbol, start=start, end=end)

# Ensure the 'Close' column has data and is valid
if 'Close' not in ds.columns:
    raise ValueError("The 'Close' column is not present in the data.")

# Normalize the data
sc = MinMaxScaler()
train_set = sc.fit_transform(ds['Close'].values.reshape(-1, 1))
print(train_set)
# Create the training dataset
past_days = 30

def prepare_data(timeseries_data, n_features):
    X, y = [], []
    for i in range(len(timeseries_data)):
        # find the end of this pattern
        end_ix = i + n_features
        # check if we are beyond the sequence
        if end_ix > len(timeseries_data)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = timeseries_data[i:end_ix], timeseries_data[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


# define input sequence
timeseries_data = ds['Close'][:6100].tolist()
# choose a number of time steps
n_steps = past_days
# split into samples
X, y = prepare_data(timeseries_data, n_steps)

# Print the shape of X before reshaping
print("Shape of X before reshaping:", X.shape)

# Check if X is empty or has incorrect dimensions
if X.size == 0:
    raise ValueError("Prepared data X is empty. Check the data preparation steps.")
if len(X.shape) != 2:
    raise ValueError("Prepared data X does not have the expected number of dimensions.")

# Reshape X for LSTM [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))

# Print the shape of X after reshaping
print("Shape of X after reshaping:", X.shape)

# Build the LSTM model
print("building model")
callback = [EarlyStopping(monitor='loss', mode='auto')]
model = Sequential()
model.add(LSTM(64, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
model.add(LSTM(64, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Fit model
model.fit(X, y, epochs=30, verbose=1, callbacks=callback)

print("saving data...")

# Save the model to JSON and weights
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# Serialize weights to HDF5
model.save_weights("model_weights.weights.h5")
print("Saved model to disk")
