import pandas as pd
import numpy as np
import yfinance as yf


# =====================================================
# Helper: Calculate Metrics for One Ticker
# =====================================================

def calculate_metrics(ticker, k=1.5, drawdown_limit=0.2):

    try:
        data = yf.download(ticker, period="1y", progress=False)

        if data.empty or len(data) < 50:
            return None

        data["Returns"] = data["Close"].pct_change()

        # -----------------------------
        # Trend Score (simple EMA logic)
        # -----------------------------
        data["EMA50"] = data["Close"].ewm(span=50).mean()
        data["EMA200"] = data["Close"].ewm(span=200).mean()

        trend_score = (
            1 if data["EMA50"].iloc[-1] > data["EMA200"].iloc[-1]
            else 0
        )

        # -----------------------------
        # Volatility / Risk
        # -----------------------------
        volatility = float(data["Returns"].std())

        # -----------------------------
        # Max Drawdown
        # -----------------------------
        cumulative = (1 + data["Returns"].fillna(0)).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative / running_max - 1).min()
        drawdown = float(drawdown)

        # Filter by drawdown limit
        if abs(drawdown) > drawdown_limit:
            return None

        # -----------------------------
        # Final Score (robust float math)
        # -----------------------------
        final_score = (
            float(trend_score) * k
            - abs(drawdown)
            - volatility
        )

        return {
            "ticker": ticker,
            "TrendScore": float(trend_score),
            "Volatility": volatility,
            "MaxDrawdown": drawdown,
            "FinalScore": final_score
        }

    except Exception:
        return None


# =====================================================
# Main Recommendation Function
# =====================================================

def generate_recommendations(tickers, k=1.5, drawdown_limit=0.2):

    results = []

    for ticker in tickers:

        metrics = calculate_metrics(
            ticker,
            k=k,
            drawdown_limit=drawdown_limit
        )

        if metrics is not None:
            results.append(metrics)

    if not results:
        return pd.DataFrame()

    results_df = pd.DataFrame(results)

    # Ensure numeric types (safety)
    for col in ["TrendScore", "Volatility", "MaxDrawdown", "FinalScore"]:
        results_df[col] = pd.to_numeric(results_df[col], errors="coerce")

    # Drop invalid rows
    results_df = results_df.dropna(subset=["FinalScore"])

    # Sort safely
    results_df = results_df.sort_values(
        by="FinalScore",
        ascending=False
    )

    return results_df