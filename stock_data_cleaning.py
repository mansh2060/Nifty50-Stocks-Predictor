import pandas as pd
import os


def get_stock_cleaned_data(stock_ticker_dict):
    """
    Cleans raw stock CSV data and generates feature-engineered datasets.

    Parameters:
        stock_ticker_dict (dict): {stock_name: ticker}

    Returns:
        list: List of cleaned file names
    """

    cleaned_files = []

    for stock in stock_ticker_dict.keys():

        # 📂 File paths
        csv_file = os.path.join("stock_data", f"{stock}.csv")
        cleaned_file = f"Cleaned_{stock}.csv"

        # ✅ Use cached cleaned file (IMPORTANT OPTIMIZATION)
        if os.path.exists(cleaned_file):
            print(f"📂 Using cached cleaned file: {cleaned_file}")
            cleaned_files.append(cleaned_file)
            continue

        # ❌ Check if raw data exists
        if not os.path.exists(csv_file):
            print(f"❌ {csv_file} not found")
            continue

        print(f"🧹 Cleaning data for {stock}...")

        # 📥 Load data
        df = pd.read_csv(csv_file)
        numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = (
                            df[col]
                            .astype(str)
                            .str.replace(",", "")   # remove commas
                            .str.replace(" ", "")
                            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # ---------------- CLEANING ----------------
        df = df.drop(index=[0, 1], errors="ignore")  # Remove unwanted rows
        df = df.reset_index(drop=True)

        # Ensure Date column

        
        df["Date"] = pd.to_datetime(df["Date"])

        # ---------------- BASIC FEATURES ----------------
        df["Yesterday Close"] = df["Close"].shift(1)
        df["Yesterday High"] = df["High"].shift(1)
        df["Yesterday Low"] = df["Low"].shift(1)
        df["Yesterday Volume"] = df["Volume"].shift(1)

        df["Today Open"] = df["Open"]
        df["Today Close"] = df["Close"]

        # ---------------- ADVANCED FEATURES ----------------

        # Returns
        df["Return"] = df["Close"].pct_change()

        # Moving averages
        df["MA_5"] = df["Close"].rolling(5).mean()
        df["MA_20"] = df["Close"].rolling(20).mean()

        # RSI
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        ema12 = df["Close"].ewm(span=12).mean()
        ema26 = df["Close"].ewm(span=26).mean()
        df["MACD"] = ema12 - ema26

        # Lag features
        for lag in [1, 2, 3, 5, 10]:
            df[f"lag_{lag}"] = df["Close"].shift(lag)

        # ---------------- TARGET ----------------
        df["Target"] = df["Return"].shift(-1)

        # ---------------- FINAL CLEAN ----------------
        df = df.dropna().reset_index(drop=True)

        # Select features
        df = df[
            [
                "Date",
                "Yesterday Close",
                "Yesterday High",
                "Yesterday Low",
                "Yesterday Volume",
                "Today Open",
                "Today Close",
                "Return",
                "MA_5",
                "MA_20",
                "RSI",
                "MACD",
                "lag_1",
                "lag_2",
                "lag_3",
                "lag_5",
                "lag_10",
                "Target",
            ]
        ]

        # Fill any remaining NaNs safely
        if df.isnull().values.any():
            df = df.fillna(df.mean(numeric_only=True))

        # 💾 Save cleaned file
        df.to_csv(cleaned_file, index=False)
        cleaned_files.append(cleaned_file)

        print(f"✅ Saved cleaned file: {cleaned_file}")

    return cleaned_files


# ---------------- TESTING BLOCK ----------------
if __name__ == "__main__":
    from stock_tickers import get_stock_ticker
    from tickers import nifty50_tickers

    ticker_dict = get_stock_ticker(nifty50_tickers, stock_name="Cipla")
    print("Selected:", ticker_dict)

    cleaned = get_stock_cleaned_data(ticker_dict)
    print("Cleaned files:", cleaned)