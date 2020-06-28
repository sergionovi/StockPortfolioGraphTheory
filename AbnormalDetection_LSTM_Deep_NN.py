# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 08:08:18 2020
Objectives:
    1 - Remove abnormal with LSTM data from stock time series.
    The main idea of the project is not only remove outliers, but also 
    learn and get in touch with LSTM deep Neural Networks. 
    
        Required Libraries:           
            numpy
            matplotlib
            pandas
            keras
            math
            
@author: Sergio Novi, sergiolnovi@gmail.com

"""
# Importing usefull libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers.core import Dense, Activation, Dropout
import time #helper libraries
import scipy.io




# Tranform time series into Data set
def create_dataset(dataset, look_back):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back)]
		dataX.append(a)
		dataY.append(dataset[i + look_back])
        
	return np.array(dataX), np.array(dataY)


def OutlierDetection(TimeSeries,look_back=7):
    # INPUT: 
        #TimeSeries: Origial time series        
        #look_back: Number of past time points to make predictions
    
    
    # Step 1 - Normalize Time Series 
    # Convert to Numpy 
    TimeSeries = np.asanyarray(TimeSeries); 
    TimeSeries = TimeSeries/np.max(np.abs(TimeSeries))

    # Step 2 - Separate data set for trainning 
    # I will take only the begining of the time series, 
    # or eventually the whole time series
    
    # Data will be predicted based on the last N points given by lookback
    trainX, trainY = create_dataset(TimeSeries, look_back)

    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))


    # create and fit the LSTM network, optimizer=adam, 25 neurons, dropout 0.1
    model = Sequential()    
    model.add(LSTM(25, input_shape=(1, look_back)))
    #model.add(Dropout(0.1))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')
    model.fit(trainX, trainY, epochs=1000, batch_size=50, verbose=1)

    trainX, trainY = create_dataset(TimeSeries, look_back)
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    trainPredict = model.predict(trainX);

    testX,testY = create_dataset(TimeSeries, look_back)

    # reshape input to be [samples, time steps, features]
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    testPredict = model.predict(testX);



    testPredict = np.squeeze(testPredict)
    testY = np.squeeze(testY)

    #Normalize Prediction
    #testPredict = testPredict/np.max(testPredict)

    error = np.abs(testY-testPredict)
    #error = error/np.min([testPredict,testY],axis=0)
    error=(error/testY)*100
    
    lst = np.zeros(len(TimeSeries));
    lst[np.where(error>=2.5)]=1;
    


    
    return error,lst


# Load the previous downloaded data 
data = pd.read_csv('HistoricalData.csv');

# I will first normalize the data. 
# As I am going to use the data for connectivity analysis, 
# this is a good practice.

dataNormalized = data.copy()
for item in data:
    if not item=='Date':
        dataNormalized[item] = data[item]/data[item].max();







