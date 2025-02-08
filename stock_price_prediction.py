# .py file call , nifty 50 stocks all connected 
from nifty50_tickers import nifty50_tickers  # stocks ---> ticker
from stock_tickers import get_stock_ticker          # return dict stock : tickers
from stock_data_fetch import get_stock_data_csv     # stock data fetch using ticker store stock.csv
from stock_data_cleaning import get_stock_cleaned_data  # csv clean return cleaned_stock.csv
from stock_data_visualisation import get_stock_price_visualisation  # selected stock data visualisation
from stock_training import get_stock_training
from stock_prediction_date import trading_day
import pandas as pd
import numpy as np

stock_ticker_dict=get_stock_ticker(nifty50_tickers)
stock=stock_ticker_dict.keys()
get_stock_data_csv(stock_ticker_dict)
stock,cleaned_file=get_stock_cleaned_data(stock_ticker_dict)
get_stock_price_visualisation(stock,cleaned_file)
model=get_stock_training(stock,cleaned_file)


cleaned_file="".join(cleaned_file)
df=pd.read_csv(cleaned_file)
prediction_date=df["Date"].max()
trading_day_name=trading_day(prediction_date)

prediction_data=df[df["Date"] == prediction_date]
print(prediction_data)

yesterday_close=df["Yesterday Close"].iloc[-1]
yesterday_high=df["Yesterday High"].iloc[-1]
yesterday_low=df["Yesterday Low"].iloc[-1]
yesterday_volume=df["Yesterday Volume"].iloc[-1]
today_open=df["Today Open"].iloc[-1]

value_array=np.array([[yesterday_close,yesterday_high,yesterday_low,yesterday_volume,today_open]])
print(value_array)
predicted_price=model.predict(value_array)
print(f"{trading_day_name}: {predicted_price}")