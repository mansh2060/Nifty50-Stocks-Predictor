import streamlit as st
import pandas as pd

# Your modules
from stock_tickers import get_stock_ticker
from stock_data_cleaning import get_stock_cleaned_data
from stock_training import get_stock_training
from stock_price_prediction import get_stock_predicted
from backtesting import backtest_model, plot_backtest
from stock_data_visualisation import get_live_stock_price

from tickers import nifty50_tickers


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Quant Trading Dashboard", layout="wide")

st.title("📈 AI-Based Quant Trading System (NIFTY 50)")

# ---------------- STOCK SELECTION ----------------
stock = st.selectbox("Select Stock", list(nifty50_tickers.keys()))


# ---------------- CACHE MODEL ----------------
@st.cache_resource
def load_model(stock, cleaned_files):
    return get_stock_training(stock, cleaned_files)


# ---------------- MAIN BUTTON ----------------
if st.button("Run Analysis 🚀"):

    # ---------------- GET TICKER ----------------
    ticker_dict = get_stock_ticker(nifty50_tickers, stock)

    if not ticker_dict:
        st.error("Invalid stock selected")
        st.stop()

    # ---------------- CLEANING ----------------
    st.info("📂 Loading & Processing Data...")
    cleaned_files = get_stock_cleaned_data(ticker_dict)

    if not cleaned_files:
        st.error("❌ No cleaned data available. Check your stock_data folder.")
        st.stop()

    # ---------------- MODEL TRAINING (CACHED) ----------------
    st.info("🤖 Training Model...")
    model = load_model(stock, cleaned_files)

    # ---------------- PREDICTION ----------------
    result = get_stock_predicted(model, cleaned_files)

    st.subheader("📊 Prediction Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Price", round(result["current_price"], 2))
    col2.metric("Predicted Price", round(result["predicted_price"], 2))

    # Signal coloring
    signal_color = "green" if result["signal"] == "BUY" else "red"
    col3.markdown(f"### Signal: <span style='color:{signal_color}'>{result['signal']}</span>", unsafe_allow_html=True)

    st.write(f"📉 Predicted Return: {result['predicted_return']:.5f}")

    # ---------------- LIVE PRICE ----------------
    st.subheader("📈 Live Price Movement")

    try:
        get_live_stock_price(ticker_dict[stock], cleaned_files)
    except:
        st.warning("⚠️ Live data not available (API issue).")

    # ---------------- BACKTEST ----------------
    st.subheader("📉 Backtesting Performance")

    df_backtest = backtest_model(model, cleaned_files)

    plot_backtest(df_backtest, stock)

    # ---------------- METRICS ----------------
    st.subheader("📊 Strategy Metrics")

    final_return = df_backtest["cumulative_strategy"].iloc[-1]
    market_return = df_backtest["cumulative_market"].iloc[-1]

    col1, col2 = st.columns(2)

    col1.metric("Strategy Return", f"{final_return:.2f}")
    col2.metric("Market Return", f"{market_return:.2f}")

    # Alpha (extra)
    alpha = final_return - market_return
    st.write(f"📌 Alpha (Outperformance): {alpha:.2f}")