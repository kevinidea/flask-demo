from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import datetime as dt
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

def getUserInput():
#get user input
    #get the stock ticker and make it uppercase
    stockTicker = 'Yahoo'.upper()
    #turn checked features into a list
    features = ['Open', 'High', 'Close']
    return stockTicker, features

def processData(stockTicker):
#get relevant financial data from QUANDL based on user input

    #get latest 90 days
    now = dt.datetime.now()
    endDate = now.strftime('%Y-%m-%d') 
    startDate = (now - dt.timedelta(days=90)).strftime('%Y-%m-%d')
    
    #get data from QUANDL
    link = 'https://www.quandl.com/api/v3/datasets/WIKI/'+stockTicker+'.json?start_date='+startDate+'&end_date='+endDate+'&order=asc&api_key=jELib4RsD4dQwp-sUVLy'
    jsonData = requests.get(link)
    
    # convert jsonData into dataframe
    dfData = pd.DataFrame(jsonData.json())
    
    #extract relevant data
    values = dfData.ix['data', 'dataset'] #list of list
    columnNames = dfData.ix['column_names','dataset'] #list of string
    relevantData = pd.DataFrame(values, columns = columnNames)
    
    #set date as index and convert date to actual date format
    relevantData = relevantData.set_index(['Date'])
    relevantData.index = pd.to_datetime(relevantData.index)
    
    return relevantData
    
def createPlot(data, features):
# reate a Bokeh plot from the dataframe
    plot = figure(x_axis_type = "datetime")
    if 'Open' in features:
        plot.line(data.index, data['Open'], color='green', legend='Opening Price')
    if 'High' in features:
        plot.line(data.index, data['High'], color='red', legend='Highest Price')
    if 'Low' in features:
        plot.line(data.index, data['Low'], color ='blue', legend = 'Lowest Price')
    if 'Close' in features:
        plot.line(data.index, data['Close'], color='black', legend='Closing Price')
    
    return plot

stockTicker, features = getUserInput()
data = processData(stockTicker)
chart = createPlot(data, features)
script, div = components(chart)