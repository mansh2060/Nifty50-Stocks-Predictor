

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
def get_stock_price_visualisation(stock,cleaned_file):
    cleaned_file="".join(cleaned_file)
    try:
        if os.path.exists(cleaned_file):
            df=pd.read_csv(cleaned_file)
            print(df.head())
            df["Date"]=pd.to_datetime(df["Date"])
            sns.lineplot(data=df,x='Date',y='Yesterday Close')
            plt.xlabel("Date")
            plt.ylabel("Yesterday Close ")
            plt.show()
            sns.lineplot(data=df,x='Date',y='Today Close')
            plt.xlabel("Date")
            plt.ylabel("Today Close")
            plt.show()
            numerical_data=df[["Yesterday Close","Yesterday High","Yesterday Low","Yesterday Volume","Today Open","Today Close"]]
            corr=numerical_data.corr()
            sns.heatmap(corr,annot=True,cmap='coolwarm')
            plt.title(f"{stock} Price Correlation")
            plt.show()
            sns.scatterplot(data=df,x='Yesterday Volume',y='Today Close')
            plt.title(f"{stock} Volume VS Price Correlation")
            plt.xlabel("Yesterday Volume")
            plt.ylabel("Today Close")
            plt.show()
    except:
        print(f"{stock} doesnot fall in Nifty 50")
    