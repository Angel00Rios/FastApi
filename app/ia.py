# Redes Neuronales Recurrentes (RNR)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart store API.

#----------------------------------------------------------------------------------------
# Description      : AI rnr module.
#                    Modules and code for Python Python 3.9
#
# Requirements.    : sklearn
#                    keras
#                    pandas
#----------------------------------------------------------------------------------------
"""

# Log Handling.
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

# Logging configuration will be __main__ as this code should run by itself.
LOG = logging.getLogger(__name__)

def get_ai(dataset_train):
    # Parte 1 - Preprocesado de los datos
    dataset_train = pd.DataFrame(dataset_train)[["Fecha", "Cantidad"]]
    dataset_train['Cantidad'] = dataset_train['Cantidad'].astype(int)
    training_set  = dataset_train.iloc[:, 1:2].values

    # Escalado de características
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Crear una estructura de datos con 60 timesteps y 1 salida
    X_train = []
    y_train = []
    for i in range(60, len(training_set_scaled)):
        X_train.append(training_set_scaled[i-60:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Redimensión de los datos
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Parte 2 - Construcción de la RNR
    # Inicialización del modelo
    regressor = Sequential()

    # Añadir la primera capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1) ))
    regressor.add(Dropout(0.1))

    # Añadir la segunda capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50, return_sequences = True ))
    regressor.add(Dropout(0.1))

    # Añadir la tercera capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50, return_sequences = True ))
    regressor.add(Dropout(0.1))

    # Añadir la cuarta capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50))
    regressor.add(Dropout(0.1))

    # Añadir la capa de salida
    regressor.add(Dense(units = 1))

    # Compilar la RNR
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

    # Ajustar la RNR al conjunto de entrenamiento
    regressor.fit(X_train, y_train, epochs = 200, batch_size = 32)

    # Parte 3 - Ajustar las predicciones y visualizar los resultados
    dataset_total = dataset_train['Cantidad'].copy()
    inputs = dataset_total[len(dataset_total) - 90:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    LOG.info(inputs)
    X_test = []
    for i in range(60, 90):
        X_test.append(inputs[i-60:i, 0])
    LOG.info(X_test)
    X_test = np.array(X_test)
    LOG.info(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    predicted_df = pd.DataFrame(predicted_stock_price)
    return {'Prediccion': predicted_df['Cantidad'].sum()}
