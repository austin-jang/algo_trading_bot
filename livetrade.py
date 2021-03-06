#Raw Package
import pandas as pd
import numpy as np

#Data Source
import yfinance as yf

#Data visualization
import plotly.graph_objs as go

#Define start and end date
sdate = pd.to_datetime('2021-01-01')
edate = pd.to_datetime('2022-01-01')

data = yf.download(
    tickers = 'BTC-USD',
    start = sdate,
    end = edate,
    #period = '5d',
    interval = '1d'
)
data

data['MA5'] = data['Close'].rolling(5).mean()
data['MA20'] = data['Close'].rolling(20).mean()

#Declare figure
fig = go.Figure()

#Setup Trace
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

fig.add_trace(
    go.Scatter(
        x = data.index,
        y = data['MA5'],
        line = dict(
            color = 'red',
            width = 1.5
        ),
        name = 'MA5'
    )
)

fig.add_trace(
    go.Scatter(
        x = data.index,
        y = data['MA20'],
        line = dict(
            color = 'green',
            width = 1.5
        ),
        name = 'MA20'
    )
)

#Show
fig.show()
