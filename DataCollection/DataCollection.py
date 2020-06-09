# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:24:20 2020

Status: Able to get Bovespa Components

Objectives:
    1 - Data Collection:
        Download and create a csv file with historical data 
        from all components (stocks) from bovespa.
    
        Required Libraries:
            requests
            lxlm
            Pandas
            yfinance 
            yahoofinancials
        
@author: Sergio Novi, sergiolnovi@gmail.com
"""
import requests
from lxml import html
import yfinance as yf 
import pandas as pd
import os

# Step 1: Web-Scrap the list of all Bovespa components.
# We will need this list to download the data with yfinance

# Get page content from specific url
url = 'https://topforeignstocks.com'
url = url+'/indices/components-of-the-bovespa-index/';
pageContent = requests.get(url);

# Store the contents under tree
tree = html.fromstring(pageContent.content)

# Take the data from the website table 
# ATTENTION: (this may not work if the website layout changes) 
table = tree.xpath('//*[@id="tablepress-2953"]/tbody')


bovespaComponents=[];
for i in range(len(table[0])):
    adress = '//*[@id="tablepress-2953"]/tbody/tr['
    adress = adress + str(i+1) + ']/td[3]/text()';
    
    bovespaComponents.append(tree.xpath(adress)[0]);

# With the list of bovespa stocks at hand, we will collect data 
# using the yfnince library. For now, we will get download all data
# from the maximum possible period per stock, but we will only 
# save the data the Open Value. As we are going to correlate the 
# stock prices over a long period of time, we do not need to worry 
# with within day oscillations.     
    
frames=[];
for item in bovespaComponents:   
    frames.append(yf.download(item+'.SA',period='max')['Open']);

data = pd.DataFrame(pd.concat(frames, keys=bovespaComponents));

# Save the data in the current folder
path = os.getcwd()
data.to_csv (rpath, index = False, header=True)
