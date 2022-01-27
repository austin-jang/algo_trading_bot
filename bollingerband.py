#Raw Package
import pandas as pd
import numpy as np

#Data Source
import yfinance as yf

#Data visualization
import plotly.graph_objs as go

data = yf.download(
    tickers = 'SPY',
    period = '1d',
    interval = '1m'
)

#1 Minute Interval Required
data['Middle Band'] = data['Close'].rolling(window = 21).mean()
data['Upper Band'] = data['Middle Band'] + 1.96*data['Close'].rolling(window = 21).std()
data['Lower Band'] = data['Middle Band'] - 1.96*data['Close'].rolling(window = 21).std()

#Declare figure
fig = go.Figure()

#Setup Trace
fig.add_trace(
    go.Scatter(
        x = data.index,
        y = data['Middle Band'],
        line = dict(
            color = 'blue',
            width = 1.5
        ),
        name = 'Middle Band'
    )
)

fig.add_trace(
    go.Scatter(
        x = data.index,
        y = data['Upper Band'],
        line = dict(
            color = 'red',
            width = 1.5
        ),
        name = 'Upper Band'
    )
)

fig.add_trace(
    go.Scatter(
        x = data.index,
        y = data['Lower Band'],
        line = dict(
            color = 'green',
            width =1.5
        ),
        name = 'Lower Band'
    )
)

#Customize Candlestick
fig.add_trace(
    go.Candlestick(
        x = data.index,
        open = data['Open'],
        high = data['High'],
        low = data['Low'],
        close = data['Close'],
        name = 'Market Data'
    )
)

#Add Titles
fig.update_layout(
    title = 'SP500 Live Share Price',
    yaxis_title = 'Stock Price (USD per Shares)'
)

#X-Axes
fig.update_xaxes(
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = list([
            dict(count = 15, label = "15m", step = "minute", stepmode = "backward"),
            dict(count = 45, label = "45m", step = "minute", stepmode = "backward"),
            dict(count = 1, label = "HTD", step = "hour", stepmode = "todate"),
            dict(count = 3, label = "3h", step = "hour", stepmode = "backward"),
            dict(step = "all")
        ])
    )
)

#Show
fig.show()
