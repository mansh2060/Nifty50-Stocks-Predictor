import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns



def get_stock_price_visualisation(stock, cleaned_file):
    try:
        # Handle file properly
        if isinstance(cleaned_file, list):
            cleaned_file = cleaned_file[0]

        if not os.path.exists(cleaned_file):
            print(f"{cleaned_file} not found")
            return

        df = pd.read_csv(cleaned_file)
        df["Date"] = pd.to_datetime(df["Date"])

        # ---------------- BASIC PRICE PLOT ----------------
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=df, x='Date', y='Today Close')
        plt.title(f"{stock} Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.show()

        # ---------------- MOVING AVERAGES ----------------
        if "MA_5" in df.columns and "MA_20" in df.columns:
            plt.figure(figsize=(10, 4))
            plt.plot(df["Date"], df["Today Close"], label="Close")
            plt.plot(df["Date"], df["MA_5"], label="MA 5")
            plt.plot(df["Date"], df["MA_20"], label="MA 20")
            plt.legend()
            plt.title(f"{stock} Moving Averages")
            plt.show()

        # ---------------- RSI ----------------
        if "RSI" in df.columns:
            plt.figure(figsize=(10, 3))
            plt.plot(df["Date"], df["RSI"])
            plt.axhline(70, linestyle='--')
            plt.axhline(30, linestyle='--')
            plt.title(f"{stock} RSI Indicator")
            plt.show()

        # ---------------- CORRELATION ----------------
        numerical_cols = df.select_dtypes(include='number')
        plt.figure(figsize=(8, 6))
        sns.heatmap(numerical_cols.corr(), annot=False, cmap='coolwarm')
        plt.title(f"{stock} Feature Correlation")
        plt.show()

        # ---------------- RETURNS DISTRIBUTION ----------------
        if "Return" in df.columns:
            plt.figure(figsize=(6, 4))
            sns.histplot(df["Return"], bins=50, kde=True)
            plt.title(f"{stock} Return Distribution")
            plt.show()

    except Exception as e:
        print(f"Error for {stock}: {e}")


# ---------------- 🚀 NEW: LIVE PRICE FUNCTION ----------------

import yfinance as yf
import streamlit as st

def get_live_stock_price(ticker, cleaned_file):
    import time

    if isinstance(cleaned_file, list):
        cleaned_file = cleaned_file[0]

    df = pd.read_csv(cleaned_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # Take last 100 points
    df = df.tail(100).reset_index(drop=True)

    st.subheader("📈 Simulated Live Price")

    chart = st.empty()

    temp_df = pd.DataFrame()

    for i in range(len(df)):
        temp_df = pd.concat([temp_df, df.iloc[[i]]])
        chart.line_chart(temp_df.set_index("Date")["Today Close"])
        time.sleep(0.05)  # speed control