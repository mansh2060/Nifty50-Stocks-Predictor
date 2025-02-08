import pandas as pd
import os
def get_stock_cleaned_data(stock_ticker_dict):
    cleaned_files=[]
    for stock,_ in stock_ticker_dict.items():
        csv_file=f"{stock}.csv"
        filename=f"Cleaned_{stock}.csv"
        if os.path.exists(filename):
                os.remove(filename)
                
        try:
            df=pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"{csv_file} doesn't exist")
            continue

        print(df.head())
        df=df.drop(index=0)
        df=df.drop(index=1)
        df=df.reset_index(drop=True)
        df=df.rename(columns={"Price":"Date"})
        print(df.head())
        df["Date"]=pd.to_datetime(df["Date"])
        df["Yesterday Close"]=df["Close"].shift(1)
        df["Yesterday High"]=df["High"].shift(1)
        df["Yesterday Low"]=df["Low"].shift(1)
        df["Yesterday Volume"]=df["Volume"].shift(1)
        df["Today Open"]=df["Open"]
        df["Today Close"]=df["Close"]
        df=df.dropna()
        df=df.reset_index(drop=True)
        print(df.head())
        print(df.columns)
        df=pd.concat([df.iloc[: , 0] , df.iloc[:,6:12]],axis=1)
        if df.isnull().values.any():
            df=df.fillna(df.mean(), inplace=True)
        print(df.head())
        df.to_csv(filename,index=False)
        cleaned_files.append(filename)

    return stock,cleaned_files
            



        