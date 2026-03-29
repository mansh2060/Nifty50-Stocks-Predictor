import pandas as pd
import numpy as np

def add_technical_indicators(df):
    df = df.copy()

    # Returns
    df['return'] = df['Close'].pct_change()

    # Moving averages
    df['ma_5'] = df['Close'].rolling(5).mean()
    df['ma_20'] = df['Close'].rolling(20).mean()

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df['Close'].ewm(span=12).mean()
    ema26 = df['Close'].ewm(span=26).mean()
    df['macd'] = ema12 - ema26

    # Bollinger Bands
    rolling_mean = df['Close'].rolling(20).mean()
    rolling_std = df['Close'].rolling(20).std()
    df['bb_upper'] = rolling_mean + 2 * rolling_std
    df['bb_lower'] = rolling_mean - 2 * rolling_std

    # Lag features
    for lag in [1, 2, 3, 5, 10]:
        df[f'lag_{lag}'] = df['Close'].shift(lag)

    df.dropna(inplace=True)
    return df