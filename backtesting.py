import pandas as pd
import numpy as np


def backtest_model(model, cleaned_file):

    if isinstance(cleaned_file, list):
        cleaned_file = cleaned_file[0]

    df = pd.read_csv(cleaned_file)

    # ---------------- FEATURES ----------------
    X = df.drop(columns=["Date", "Target"], errors="ignore")

    # ---------------- PREDICTIONS ----------------
    df["predicted_return"] = model.predict(X)

    # ---------------- SIGNALS ----------------
    threshold = 0.002  # 0.2%

    df["signal"] = 0
    df.loc[df["predicted_return"] > threshold, "signal"] = 1   # BUY
    df.loc[df["predicted_return"] < -threshold, "signal"] = -1 # SELL

    # ---------------- STRATEGY RETURNS ----------------
    df["strategy_return"] = df["signal"].shift(1) * df["Return"]

    # ---------------- CUMULATIVE RETURNS ----------------
    df["cumulative_strategy"] = (1 + df["strategy_return"]).cumprod()
    df["cumulative_market"] = (1 + df["Return"]).cumprod()

    # ---------------- METRICS ----------------
    sharpe = np.mean(df["strategy_return"]) / np.std(df["strategy_return"]) * np.sqrt(252)

    max_drawdown = (
        df["cumulative_strategy"].cummax() - df["cumulative_strategy"]
    ).max()

    final_return = df["cumulative_strategy"].iloc[-1]

    print(f"Final Strategy Return: {final_return}")
    print(f"Sharpe Ratio: {sharpe}")
    print(f"Max Drawdown: {max_drawdown}")

    return df

import matplotlib.pyplot as plt

def plot_backtest(df, stock_name):

    plt.figure(figsize=(10, 5))

    plt.plot(df["cumulative_strategy"], label="Strategy")
    plt.plot(df["cumulative_market"], label="Market (Buy & Hold)")

    plt.title(f"{stock_name} Strategy vs Market")
    plt.legend()
    plt.show()