# Import TF libraries and data query files
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import GetIdealColor # Ideal color loaded from database
import getIrrigation # Irrigation volumes loaded from database

# Create data sets from data query functions from database
# Currently, the model is formatted for consistent data input/output from database
# To format model for environmental data from NASA PhenoCam, switch data functions to csv file reads
(x_train, y_train), (x_test, y_test) = getIrrigation.getIrrigation(), GetIdealColor.idealColor()
x_train, x_test = x_train / 255.0, x_test / 255.0
sample, sample_label = x_train[0], y_train[0]

# Create model
model = keras.Sequential()

# Input Layer
model.add(layers.Embedding(input_dim=1000, output_dim=64))

# LSTM Layer
model.add(layers.LSTM(128))

# Dense Layer
model.add(layers.Dense(10))

# Bidirectional layers for LSTM backprop
model.add(
    layers.Bidirectional(layers.LSTM(64, return_sequences=True), input_shape=(5, 10))
)
model.add(layers.Bidirectional(layers.LSTM(32)))
model.add(layers.Dense(10))

# Build the RNN model
def build_model(allow_cudnn_kernel=True):

    units = 64
    input_dim = 28
    output_size = 10    

    if allow_cudnn_kernel:
        # Default RNN LSTM Layer
        lstm_layer = keras.layers.LSTM(units, input_shape=(None, input_dim))
    else:
        lstm_layer = keras.layers.RNN(
            keras.layers.LSTMCell(units), input_shape=(None, input_dim)
        )
    model = keras.models.Sequential(
        [
            lstm_layer,
            keras.layers.BatchNormalization(),
            keras.layers.Dense(output_size),
        ]
    )

    # Fit the model on training data and return model
    model.fit(x_train, y_train)

    return model


