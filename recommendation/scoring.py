import pandas as pd
import numpy as np


# ==============================
# Trend Score
# ==============================

def calculate_trend_score(df):

    # Beispiel: einfache Momentum-Bewertung
    df["returns_20"] = df["Close"].pct_change(20)

    trend_score = df["returns_20"].iloc[-1]

    return trend_score


# ==============================
# Risk Score (ATR-basiert)
# ==============================

def calculate_risk_score(df, atr_window=14):

    df["high_low"] = df["High"] - df["Low"]
    df["high_close"] = abs(df["High"] - df["Close"].shift())
    df["low_close"] = abs(df["Low"] - df["Close"].shift())

    tr = df[["high_low", "high_close", "low_close"]].max(axis=1)
    atr = tr.rolling(atr_window).mean()

    current_atr = atr.iloc[-1]

    risk_score = current_atr / df["Close"].iloc[-1]

    return risk_score