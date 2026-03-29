#here i need to create a dictionary containig stocks along with its tickers  
nifty50_tickers = {
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Ports & SEZ": "ADANIPORTS.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    
}

import yfinance as yf
from datetime import datetime
start_date = "2020-01-01"
end_date=datetime.today().strftime('%Y-%m-%d')

for stock, ticker in nifty50_tickers.items():
  data=yf.download(tickers = ticker,start=start_date,end=end_date)
  filename = f"{stock}.csv"
  data.reset_index(inplace=True)
  data.to_csv(filename, index=False)