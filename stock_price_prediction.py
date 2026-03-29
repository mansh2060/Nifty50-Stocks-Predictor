import pandas as pd
import numpy as np


def get_stock_predicted(model, cleaned_file):
    
    # Handle file properly
    if isinstance(cleaned_file, list):
        cleaned_file = cleaned_file[0]

    df = pd.read_csv(cleaned_file)

    # Get latest row (most recent data)
    latest_row = df.iloc[-1:]

    # ---------------- FEATURES ----------------
    # Drop non-feature columns
    X = latest_row.drop(columns=["Date", "Target"], errors="ignore")

    # ---------------- PREDICTION ----------------
    predicted_return = model.predict(X)[0]

    # ---------------- SIGNAL GENERATION ----------------
    threshold = 0.002  # ~0.2% movement

    if predicted_return > threshold:
        signal = "BUY"
    elif predicted_return < -threshold:
        signal = "SELL"
    else:
        signal = "HOLD"

    # ---------------- OPTIONAL: PRICE ESTIMATE ----------------
    current_price = latest_row["Today Close"].values[0]
    predicted_price = current_price * (1 + predicted_return)

    return {
        "predicted_return": predicted_return,
        "predicted_price": predicted_price,
        "signal": signal,
        "current_price": current_price
    }