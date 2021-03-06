#Import raw packages
import pandas as pd
import numpy as np
import plotly.graph_objs as go

#Datetime package
from datetime import date

#Yahoo Finance
import yfinance as yf

#Define start and end date
start = pd.to_datetime('2021-07-01')
end = pd.to_datetime('2022-01-14')

#Set tickers
ticker = ['TWTR', 'UBER', 'SNAP', 'NFLX']

#Getting length of list
length = len(ticker)
i = 0

#Iterate using while loop
while i < length:
    print(ticker[i] + " is uploading data")
    locals()[str(ticker[i]) + "_data"] = yf.download(ticker[i], start=start, end=end)
    locals()[str(ticker[i]) + "_data"].to_csv(str(ticker[i]) + "_data.csv")
    i += 1

TWTR_data

#Check head and tail of your data
TWTR_data.head()

#Tail Data
TWTR_data.tail()

#Store dataframe into CSV file
#Twitter data into a CSV File
TWTR_data.to_csv('TWTR_data.csv')
#Netflix data into a CSV File
NFLX_data.to_csv('NFLX_data.csv')
#Snapchat data into a CSV File
SNAP_data.to_csv('SNAP_data.csv')
#Uber data into a CSV File
UBER_data.to_csv('UBER_data.csv')

#Data Visualization
#Setup different Y-axis
TWTR_Close = TWTR_data['Close']
NFLX_Close = NFLX_data['Close']
SNAP_Close = SNAP_data['Close']
UBER_Close = UBER_data['Close']

TWTR_Close.head()

#Declare figure
fig = go.Figure()

#Add trace
fig.add_trace(go.Scatter(x=TWTR_data.index, y=TWTR_Close, name='Twitter'))
fig.add_trace(go.Scatter(x=NFLX_data.index, y=NFLX_Close, name='Netflix'))
fig.add_trace(go.Scatter(x=SNAP_data.index, y=SNAP_Close, name='Snapchat'))
fig.add_trace(go.Scatter(x=UBER_data.index, y=UBER_Close, name='Uber'))

#Update X and Y axis with a title name + a range slider
fig.update_xaxes(
    title = 'Date', rangeslider_visible=True
)

fig.update_yaxes(
    title = 'Stock Price (USD)'
)

#Show
fig.show()
