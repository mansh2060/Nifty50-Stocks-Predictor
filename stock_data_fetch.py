from datetime import date,timedelta
import yfinance as yf
import pandas as pd
import os
def get_stock_data_csv(stock_ticker_dict):
    start_date="2020-01-01"
    end_date=date.today() 
    for stock,ticker in stock_ticker_dict.items():
        ticker=ticker
        filename=f"{stock}.csv"
        if os.path.exists(filename):
            os.remove(filename)
        
        data=yf.download(ticker,start=start_date,end=end_date)
        return data.to_csv(filename)
 
    