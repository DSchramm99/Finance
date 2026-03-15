import pandas as pd
import numpy as np
import yfinance as yf


# =====================================================
# Indicators
# =====================================================

def add_indicators(df):
    df = df.copy()

    df["SMA20"] = df["Close"].rolling(20).mean()

    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close = np.abs(df["Low"] - df["Close"].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    return df


# =====================================================
# Backtest Engine
# =====================================================

def run_backtest(ticker, start_capital=2000):

    k = 1.5
    risk_per_trade = 200
    risk_reward = 2

    data = yf.download(
        ticker,
        period="2y",
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = add_indicators(data)

    capital = start_capital
    equity_curve = []

    position = None

    for i in range(50, len(data)):

        row = data.iloc[i]

        if pd.isna(row["ATR"]) or pd.isna(row["SMA20"]):
            equity_curve.append(capital)
            continue

        close = float(row["Close"])
        sma = float(row["SMA20"])
        atr = float(row["ATR"])

        # Trend Score Logic
        trend_raw = (close - sma) / sma
        trend_score = 50 + trend_raw * 200
        trend_score = np.clip(trend_score, 0, 100)

        # Entry
        if position is None:

            if trend_score > 65:

                entry = close
                stop = entry - (k * atr)

                risk_per_share = entry - stop

                if risk_per_share <= 0:
                    continue

                position_size = risk_per_trade / risk_per_share
                position_value = position_size * entry

                if position_value <= capital:

                    position = {
                        "entry": entry,
                        "stop": stop,
                        "size": position_size
                    }

        else:
            # Position Management

            if close <= position["stop"]:
                # Stop Loss
                capital -= (position["entry"] - position["stop"]) * position["size"]
                position = None

            elif close >= position["entry"] + risk_reward * (position["entry"] - position["stop"]):
                # Take Profit
                capital += (position["entry"] - position["stop"]) * position["size"] * risk_reward
                position = None

        equity_curve.append(capital)

    return pd.DataFrame({
        "Equity": equity_curve
    })