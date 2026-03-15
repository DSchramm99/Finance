import pandas as pd
import numpy as np
import yfinance as yf


def add_indicators(df):
    df = df.copy()

    df["SMA20"] = df["Close"].rolling(20).mean()

    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close = np.abs(df["Low"] - df["Close"].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    return df


def get_company_name(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName", ticker)
    except:
        return ticker


def generate_recommendations(tickers):

    k = 1.5
    risk_reward = 2

    results = []

    for ticker in tickers:

        try:
            data = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if data.empty:
                continue

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data = add_indicators(data)
            latest = data.iloc[-1]

            if pd.isna(latest["ATR"]) or pd.isna(latest["SMA20"]):
                continue

            close = float(latest["Close"])
            sma = float(latest["SMA20"])
            atr = float(latest["ATR"])

            # Trend Score
            trend_raw = (close - sma) / sma
            trend_score = 50 + trend_raw * 200
            trend_score = int(np.clip(trend_score, 0, 100))

            # Entry Logic
            entry = close if trend_score > 65 else sma

            # Stop
            stop = entry - (k * atr)

            risk = entry - stop
            take_profit = entry + (risk_reward * risk)

            # Risk Score (intern positiv)
            volatility = atr / close
            risk_score = 100 - (volatility * 500)
            risk_score = int(np.clip(risk_score, 0, 100))

            # Final Score
            final_score = int(
                0.6 * trend_score +
                0.4 * risk_score
            )

            results.append({
                "company_name": get_company_name(ticker),
                "ticker": ticker,
                "latest_price": close,
                "entry_price": entry,
                "stop_level": stop,
                "take_profit": take_profit,
                "trend_score": trend_score,
                "risk_score": risk_score,
                "final_score": final_score
            })

        except:
            continue

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)

    return df.sort_values("final_score", ascending=False).head(5)