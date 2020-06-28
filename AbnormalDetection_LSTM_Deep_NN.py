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


# Load the previous downloaded data 
data = pd.read_csv('HistoricalData.csv');

# I will first normalize the data. 
# As I am going to use the data for connectivity analysis, 
# this is a good practice.

dataNormalized = data.copy()
for item in data:
    if not item=='Date':
        dataNormalized[item] = data[item]/data[item].max();







