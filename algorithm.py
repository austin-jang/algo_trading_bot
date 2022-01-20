#Data manipulation
import pandas as pd
import numpy as np

#Data visualization
import plotly.graph_objs as go

#Data library
import yfinance as yf

#Download input data
start_date = '2021-01-01'
end_date = '2022-01-01'

df = yf.download('SPY', start=start_date, end=end_date)
df

#MACD
df['MA20'] = df['Close'].rolling(20).mean()
df['MA50'] = df['Close'].rolling(50).mean()
df['MA100'] = df['Close'].rolling(100).mean()

#Exponential Moving Average EWM
df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()
df

#Visualization
#Declare figure
fig = go.Figure()

#Customize Candlestick
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df['Open'], 
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='market data'
    )
)

#Customize Scatterplot
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df['EMA20'],
        name='EMA20'
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df['EMA50'],
        name='EMA50'
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df['EMA100'],
        name='EMA100'
    )
)


#Show
fig.show()