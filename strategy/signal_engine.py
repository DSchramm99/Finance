import numpy as np
import pandas as pd

# =====================================================
# Indicators
# =====================================================

def add_indicators(df):
    df = df.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()

    # ATR Calculation
    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close = np.abs(df["Low"] - df["Close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    # RSI Calculation
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

# =====================================================
# Scoring System
# =====================================================

def calculate_scores(row):
    """
    Calculates trend, risk and final scores based on the improved setup.
    """
    close = float(row["Close"])
    sma20 = float(row["SMA20"])
    sma50 = float(row.get("SMA50", 0))
    sma200 = float(row.get("SMA200", 0))
    atr = float(row["ATR"])
    rsi = float(row.get("RSI", 50))

    if pd.isna(sma20) or pd.isna(atr) or sma20 == 0 or close == 0:
        return 0, 0, 0

    # Improved Trend Score
    trend_raw = (close - sma20) / sma20
    trend_score = 50 + trend_raw * 200

    # Bonus for being above long term averages
    if not pd.isna(sma200) and close > sma200:
        trend_score += 10
    if not pd.isna(sma50) and sma20 > sma50:
        trend_score += 5
    if rsi > 50:
        trend_score += 5

    trend_score = int(np.clip(trend_score, 0, 100))

    # Risk Score (Volatility based)
    volatility = atr / close
    risk_score = int(np.clip(100 - (volatility * 500), 0, 100))

    # Final Score
    final_score = int(0.6 * trend_score + 0.4 * risk_score)

    return trend_score, risk_score, final_score

# =====================================================
# Chandelier Levels
# =====================================================

def calculate_trade_levels(price, sma20, atr, trend_score, k_atr=1.5, rr_ratio=2.0):
    """
    Determines entry, stop loss and take profit.
    """
    # Entry Logic
    if trend_score > 70: # Increased threshold for momentum entry
        entry_price = price
    else:
        entry_price = sma20

    # Stop Loss (Initial distance)
    # We use a slightly tighter ATR for entry, but chandelier trails later
    stop_level = entry_price - (k_atr * atr)

    # Take Profit
    risk_distance = entry_price - stop_level
    take_profit = entry_price + (rr_ratio * risk_distance)

    return entry_price, stop_level, take_profit

# =====================================================
# Main Signal Function
# =====================================================

def generate_signal(df, k_atr=1.5, rr_ratio=2.0):
    df = add_indicators(df)
    latest = df.iloc[-1]

    if pd.isna(latest["SMA20"]) or pd.isna(latest["ATR"]):
        return None

    trend_score, risk_score, final_score = calculate_scores(latest)

    # Improved Signal Logic
    signal = "HOLD"
    # Added RSI and Long-term trend filters
    if trend_score > 65 and risk_score > 40:
        if latest["Close"] > latest["SMA200"] and latest["RSI"] > 45:
            signal = "BUY"

    entry_price, stop_level, take_profit = calculate_trade_levels(
        float(latest["Close"]),
        float(latest["SMA20"]),
        float(latest["ATR"]),
        trend_score,
        k_atr=k_atr,
        rr_ratio=rr_ratio
    )

    # Reasoning
    reasons = []
    if latest["Close"] > latest["SMA20"]:
        reasons.append("Kurzfristiger Trend positiv (Preis > SMA20).")
    if latest["Close"] > latest["SMA200"]:
        reasons.append("Langfristiger Trend positiv (Preis > SMA200).")
    if trend_score > 65:
        reasons.append(f"Trend Score ({trend_score}) ist stark.")
    if latest["RSI"] > 50:
        reasons.append(f"Momentum ist positiv (RSI: {latest['RSI']:.1f}).")

    reason_text = " ".join(reasons)

    return {
        "signal": signal,
        "trend_score": trend_score,
        "risk_score": risk_score,
        "final_score": final_score,
        "entry_price": float(entry_price),
        "stop_level": float(stop_level),
        "take_profit": float(take_profit),
        "latest_price": float(latest["Close"]),
        "reason": reason_text
    }
