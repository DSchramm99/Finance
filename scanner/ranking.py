import yfinance as yf
import pandas as pd

from strategy.signal_engine import generate_signal


def scan_universe(universe, k=1.5):

    results = []

    for ticker in universe:

        try:
            df = yf.download(ticker, period="6mo", auto_adjust=True)

            if df.empty:
                continue

            signal_data = generate_signal(df, k=k)

            if signal_data is None:
                continue

            if signal_data["signal"] == "BUY":

                results.append({
                    "ticker": ticker,
                    "trend_score": signal_data["trend_score"],
                    "risk_score": signal_data["risk_score"],
                    "stop_level": signal_data["stop_level"],
                    "latest_price": signal_data["latest_price"]
                })

        except Exception:
            continue

    # Ranking: hohe Trendstärke zuerst
    ranked = sorted(
        results,
        key=lambda x: x["trend_score"],
        reverse=True
    )

    return ranked