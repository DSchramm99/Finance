import numpy as np
import pandas as pd
import yfinance as yf

# =====================================================
# Indicators
# =====================================================

def add_indicators(df):
    df = df.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["ATR"] = (df["High"] - df["Low"]).rolling(14).mean()
    return df

# =====================================================
# Trend Score (0-100)
# =====================================================

def calculate_trend_score(row):
    score = 0

    if row["Close"] > row["SMA20"]:
        score += 50

    if not pd.isna(row["SMA20"]) and row["SMA20"] > 0:
        distance = (row["Close"] - row["SMA20"]) / row["SMA20"]
        score += min(max(distance * 1000, 0), 30)

    return min(score, 100)

# =====================================================
# Risk Score (0-100)
# =====================================================

def calculate_risk_score(row):
    if pd.isna(row["ATR"]) or row["Close"] == 0:
        return 0

    volatility = row["ATR"] / row["Close"]
    score = 100 - (volatility * 1000)

    return max(min(score, 100), 0)

# =====================================================
# Chandelier Stop
# =====================================================

def calculate_chandelier_stop(highest_price, atr, k):
    return highest_price - (k * atr)

# =====================================================
# Position Size (optional future use)
# =====================================================

def calculate_position_size(account_equity, entry_price, stop_price):
    stop_distance = abs(entry_price - stop_price)

    if stop_distance == 0:
        return 0

    risk_per_trade = 0.02
    risk_amount = account_equity * risk_per_trade

    position_size = risk_amount / stop_distance
    return position_size

# =====================================================
# Main Signal Function
# =====================================================

def generate_signal(df, k=1.5):

    df = add_indicators(df)
    latest = df.iloc[-1]

    if pd.isna(latest["SMA20"]) or pd.isna(latest["ATR"]):
        return None

    trend_score = calculate_trend_score(latest)
    risk_score = calculate_risk_score(latest)

    signal = "HOLD"
    if trend_score > 65 and risk_score > 40:
        signal = "BUY"

    # Entry Logic
    current_price = float(latest["Close"])

    if signal == "BUY":
        entry_price = current_price
    else:
        entry_price = max(current_price, float(latest["SMA20"]))

    # Stop (Chandelier)
    highest_price = df["Close"].max()
    atr = float(latest["ATR"])
    stop_level = calculate_chandelier_stop(highest_price, atr, k)

    # ATR-based Take Profit (aligned with k)
    risk_distance = abs(entry_price - stop_level)
    take_profit = entry_price + (risk_distance * 2)

    # Reasoning
    reasons = []

    if latest["Close"] > latest["SMA20"]:
        reasons.append("Preis liegt über SMA20 (Aufwärtstrend).")

    if trend_score > 65:
        reasons.append("Starker Trend Score.")

    if risk_score > 40:
        reasons.append("Akzeptables Risikoprofil.")

    reason_text = " ".join(reasons)

    return {
        "signal": signal,
        "trend_score": float(trend_score),
        "risk_score": float(risk_score),
        "entry_price": float(entry_price),
        "stop_level": float(stop_level),
        "take_profit": float(take_profit),
        "latest_price": current_price,
        "reason": reason_text
    }