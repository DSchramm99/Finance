import numpy as np
import pandas as pd


# ==============================
# Indicators
# ==============================

def add_indicators(df):
    df = df.copy()

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["ATR"] = (df["High"] - df["Low"]).rolling(14).mean()

    return df


# ==============================
# Trend Score (0-100)
# ==============================

def calculate_trend_score(row):

    score = 0

    if row["Close"] > row["SMA20"]:
        score += 50

    if not pd.isna(row["SMA20"]) and row["SMA20"] > 0:
        distance = (row["Close"] - row["SMA20"]) / row["SMA20"]
        score += min(max(distance * 1000, 0), 30)

    return min(score, 100)


# ==============================
# Risk Score (0-100)
# ==============================

def calculate_risk_score(row):

    if pd.isna(row["ATR"]) or row["Close"] == 0:
        return 0

    volatility = row["ATR"] / row["Close"]

    score = 100 - (volatility * 1000)

    return max(min(score, 100), 0)


# ==============================
# Chandelier Stop (ATR)
# ==============================

def calculate_chandelier_stop(highest_price, atr, k):

    return highest_price - (k * atr)


# ==============================
# Position Size Logic
# ==============================

def calculate_position_size(
    account_equity,
    entry_price,
    stop_price,
    min_position_value=500
):

    stop_distance = abs(entry_price - stop_price)

    if stop_distance == 0:
        return 0

    # Risiko basiert auf Stop
    risk_per_trade = 0.02  # 2% vom Trading-Kapital maximal riskieren

    risk_amount = account_equity * risk_per_trade

    position_size = risk_amount / stop_distance

    position_value = position_size * entry_price

    # Mindestgröße beachten
    if position_value < min_position_value:
        return 0

    return position_size


# ==============================
# Main Signal Function
# ==============================

def generate_signal(
    df,
    k=1.5,
    min_position_value=500
):

    df = add_indicators(df)

    latest = df.iloc[-1]

    if pd.isna(latest["SMA20"]) or pd.isna(latest["ATR"]):
        return None

    trend_score = calculate_trend_score(latest)
    risk_score = calculate_risk_score(latest)

    signal = "HOLD"

    if trend_score > 65 and risk_score > 40:
        signal = "BUY"

    # Stop Calculation
    highest_price = df["Close"].max()
    atr = latest["ATR"]

    chandelier_stop = calculate_chandelier_stop(
        highest_price,
        atr,
        k
    )

    stop_level = chandelier_stop

    return {
        "signal": signal,
        "trend_score": trend_score,
        "risk_score": risk_score,
        "stop_level": stop_level,
        "latest_price": float(latest["Close"])
    }