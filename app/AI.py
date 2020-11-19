# Redes Neuronales Recurrentes (RNR)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart store API.

#----------------------------------------------------------------------------------------
# Description      : AI module.
#                    Modules and code for Python Python 3.9
#
# Requirements.    : sklearn
#                    keras
#                    pandas
#----------------------------------------------------------------------------------------
"""

# Importación de las librerías
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy as np
import pandas as pd
import requests
import os

headers = {'AccessKey': os.environ['AccessKey'],
           'table': 'productos'}

def backpropagation():
    # Importar el dataset de entrenamiento
    response = requests.get("/get", headers=headers)
    if response.status_code == 200:
        dataset_train = pd.DataFrame(response.json())
    training_set  = dataset_train.iloc[:, 1:2].values

    # Escalado de características
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Crear una estructura de datos con 60 timesteps y 1 salida
    X_train = []
    y_train = []
    for i in range(60, 1258):
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
    regressor.add(Dropout(0.2))

    # Añadir la segunda capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50, return_sequences = True ))
    regressor.add(Dropout(0.2))

    # Añadir la tercera capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50, return_sequences = True ))
    regressor.add(Dropout(0.2))

    # Añadir la cuarta capa de LSTM y la regulariación por Dropout
    regressor.add(LSTM(units = 50))
    regressor.add(Dropout(0.2))

    # Añadir la capa de salida
    regressor.add(Dense(units = 1))

    # Compilar la RNR
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

    # Ajustar la RNR al conjunto de entrenamiento
    regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

    # Parte 3 - Ajustar las predicciones y visualizar los resultados

    # Obtener el valor de las acciones reales  de Enero de 2017
    dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
    real_stock_price = dataset_test.iloc[:, 1:2].values

    # Obtener la predicción de la acción con la RNR para Enero de 2017
    dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
    inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, 80):
        X_test.append(inputs[i-60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

