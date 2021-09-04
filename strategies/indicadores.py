import numpy as np
import pandas as pd
import talib
from statistics import fmean, pstdev

def bbands(candles, timeperiod):
    close = np.array(candles['close'])
    return talib.BBANDS(close, timeperiod, nbdevup=2, nbdevdn=2, matype=0)

def atr(candles, timeperiod):
    high = np.array(candles["high"])
    low = np.array(candles["low"])
    close = np.array(candles['close'])
    
    return talib.ATR(high, low, close, timeperiod)[99]

def rsi(candles, timeperiod):
    close = np.array(candles["close"])
    return talib.RSI(close,timeperiod)[100]


#gera um unico valor
def personal_bbands(candles):
    k = 2
    bands = dict()
    bands['middle'] = float(fmean(candles["close"]))
    desvio_padrao = pstdev(candles["close"], bands['middle'])
    bands['upper'] = float(bands['middle']) + (desvio_padrao * k)
    bands['lower'] = float(bands['middle']) - (desvio_padrao * k)
    return bands


def personal_atr(candles, number_of_candles):
    data = pd.DataFrame({
        "High": candles['high'],
        "Close": candles['close'],
        "Low": candles['low']
    })
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)

    atr = true_range.rolling(number_of_candles).sum() / number_of_candles

    return atr