from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd


def get_stock_training(stock, cleaned_file):

    # Handle file properly
    if isinstance(cleaned_file, list):
        cleaned_file = cleaned_file[0]

    df = pd.read_csv(cleaned_file)

    print(df.head())

    # ---------------- FEATURES ----------------
    # Drop non-feature columns
    X = df.drop(columns=["Date", "Target"], errors="ignore")

    # Target = next day return
    y = df["Target"]

    # ---------------- TIME SERIES SPLIT ----------------
    split = int(len(df) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    # ---------------- MODEL ----------------
    model = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(X_train, y_train)

    # ---------------- PREDICTION ----------------
    y_pred = model.predict(X_test)

    # ---------------- METRICS ----------------
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    print(f"MAE: {mae}")
    print(f"MSE: {mse}")

    # ---------------- DIRECTIONAL ACCURACY (🔥 IMPORTANT) ----------------
    direction_accuracy = ( (y_pred > 0) == (y_test > 0) ).mean()
    print(f"Directional Accuracy: {direction_accuracy}")

    return model