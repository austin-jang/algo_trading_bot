import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import plotly.graph_objs as go

start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2021-11-01')

df = yf.download('TSLA', start_date, end_date)
df

#Ichimoku Application
index = pd.date_range(
    end_date, 
    periods = 25, 
    freq = 'D'
)
columns = df.columns
dfna = pd.DataFrame(
    index = index,
    columns = columns
)

df = pd.concat(
    [df, dfna]
)

#Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
nine_period_high = df['High'].rolling(window = 9).max()
nine_period_low = df['Low'].rolling(window = 9).min()
df['tenkan_sen'] = (nine_period_high + nine_period_low)/2

#Kijun-sen (Base Line): (26-period high + 26-period low)/2
twentysix_period_high = df['High'].rolling(window = 26).max()
twentysix_period_low = df['Low'].rolling(window = 26).min()
df['kijun_sen'] = (twentysix_period_high + twentysix_period_low)/2

#Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2
df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen'])/2).shift(26)

#Senkou Span B (Leading Span B): (52-period high + 52-period low)/2
fiftytwo_period_high = df['High'].rolling(window = 52).max()
fiftytwo_period_low = df['Low'].rolling(window = 52).min()
df['senkou_span_b'] = ((fiftytwo_period_high + fiftytwo_period_low)/2).shift(52)

#Chikou Span: The most current closing price plotted 26 time periods behind
df['chikou_span'] = df['Close'].shift(-26)
df

#Algorithm Visualization
#Declare figure
fig = go.Figure()

#Setup traces
fig.add_trace(
    go.Candlestick(
        x = df.index,
        open = df['Open'],
        high = df['High'],
        low = df['Low'],
        close = df['Close'],
        name = 'market data'
    )
)

fig.add_trace(
    go.Scatter(
        x = df.index,
        y = df['tenkan_sen'],
        line = dict(
            color = 'blue',
            width = .8
        ),
        name = 'Tenkan Sen'
    )
)

fig.add_trace(
    go.Scatter(
        x = df.index,
        y = df['kijun_sen'],
        line = dict(
            color = 'orange',
            width = .8
        ),
        name = 'Kijun Sen'
    )
)

fig.add_trace(
    go.Scatter(
        x = df.index,
        y = df['senkou_span_a'],
        line = dict(
            color = 'black',
            width = .8
        ),
        name = 'Senkou Span A'
    )
)

fig.add_trace(
    go.Scatter(
        x = df.index,
        y = df['senkou_span_b'],
        line = dict(
            color = 'purple',
            width = .8
        ),
        name = 'Senkou Span B',
        #fill = 'tonexty',
        #fillcolor = 'GREEN',
        #opacity = .1
    )
)

fig.add_trace(
    go.Scatter(
        x = df.index,
        y = df['chikou_span'],
        line = dict(
            color = 'red',
            width = .8
        ),
        name = 'Chikou Span'
    )
)

#Show
#fig.show()
fig.write_html("/Users/jangw/OneDrive/Desktop/AlgoTrading/Ichimoku.html")

#Backtesting Algorithm
#Market Condition
df.dropna(
    inplace = True
)

#Above_or_below the cloud
df['above_cloud'] = 0
df['above_cloud'] = np.where(
    (df['Low'] > df['senkou_span_a']) & (df['Low'] > df['senkou_span_a']), 1, 
    df['above_cloud']
) #Low Below 1
df['above_cloud'] = np.where(
    (df['High'] < df['senkou_span_a']) & (df['High'] < df['senkou_span_a']), -1,
    df['above_cloud']
) #High Above 1

#Senkou_Span_A above or below Senkou_Span_B
df['A_above_B'] = np.where(
    (df['senkou_span_a'] > df['senkou_span_b']), 1, -1
)

#Setting that tenkan_sen crossed up kijun_sen
df['tenkan_kijun_cross'] = 0
df['tenkan_kijun_cross'] = np.where(
    (df['tenkan_sen'].shift(1) <= df['kijun_sen'].shift(1)) & (df['tenkan_sen'] < df['kijun_sen']), 1, 
    df['tenkan_kijun_cross']
)
df['tenkan_kijun_cross'] = np.where(
    (df['tenkan_sen'].shift(1) >= df['kijun_sen'].shift(1)) & (df['tenkan_sen'] > df['kijun_sen']), -1,
    df['tenkan_kijun_cross']
)

#Setting that tenkan_sen crossed up when Open > tenkan_sen
df['price_tenkan_cross'] = 0
df['price_tenkan_cross'] = np.where(
    (df['tenkan_sen'].shift(1) <= df['Open'].shift(1)) & (df['tenkan_sen'] < df['Open']), -1,
    df['price_tenkan_cross']
)
df['price_tenkan_cross'] = np.where(
    (df['tenkan_sen'].shift(1) >= df['Open'].shift(1)) & (df['tenkan_sen'] > df['Open']), 1,
    df['price_tenkan_cross']
)
df

#Buy & Sell Signals
#Buy
df['buy'] = np.NaN
df['buy'] = np.where(
    (df['above_cloud'].shift(1) == 1) & (df['A_above_B'].shift(1) == 1) &
    ((df['price_tenkan_cross'].shift(1) == 1) | (df['tenkan_kijun_cross'].shift(1) == 1)), 1, df['buy']
)
df['buy'] = np.where(
    df['tenkan_kijun_cross'].shift(1) == -1, 0, df['buy']
)
df['buy'].ffill(
    inplace = True
)

#Sell
df['sell'] = np.NaN
df['sell'] = np.where(
    (df['above_cloud'].shift(1) == -1) & (df['A_above_B'].shift(1) == -1) &
    ((df['price_tenkan_cross'].shift(1) == -1) | (df['tenkan_kijun_cross'].shift(1) == -1)), 1, df['sell']
)
df['sell'] = np.where(
    df['tenkan_kijun_cross'].shift(1) == 1, 0, df['sell']
)
df['position'] = df['buy'] + df['sell']
df
