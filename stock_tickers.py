def get_stock_ticker(nifty50_tickers):
    tickers_dict={}
    stock_name=input("Enter the stock price             :")
    try:
        ticker=nifty50_tickers[stock_name]
        if ticker:
            tickers_dict[stock_name]= ticker
    except NameError:
        print("Stock  is not present in Nifty50")
    return tickers_dict



"""
previous day : stock price close , stock volume , stock open , stock low , stock high ,
current day  : stock price open
"""