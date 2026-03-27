import yfinance as yf
import pandas as pd
import numpy as np
import os
from backtesting.engine import run_backtest
from universe.universe_loader import get_index_universe

def verify_profitability():
    # Define markets and symbols for a diverse backtest
    indices = {
        "USA": ["S&P 500", "Nasdaq 100", "Dow Jones"],
        "Germany": ["DAX", "TecDAX"]
    }

    # Mapping for German tickers to Yahoo Finance symbols
    german_suffix = ".DE"

    # Select a diverse set of stocks from each index
    selected_stocks = []
    for region, idx_list in indices.items():
        for idx in idx_list:
            try:
                tickers = get_index_universe(idx)

                clean_tickers = []
                for t in tickers:
                    t = str(t).strip()
                    if not t or " " in t or len(t) > 10: # Basic heuristic to skip non-tickers
                        continue
                    if region == "Germany" and not t.endswith(german_suffix):
                        clean_tickers.append(t + german_suffix)
                    else:
                        clean_tickers.append(t)

                if len(clean_tickers) >= 5:
                    step = len(clean_tickers) // 5
                    selected_stocks.extend([clean_tickers[0], clean_tickers[step], clean_tickers[2*step], clean_tickers[3*step], clean_tickers[-1]])
                else:
                    selected_stocks.extend(clean_tickers)
            except Exception as e:
                print(f"Error loading {idx}: {e}")

    # Remove duplicates and filter bad ones
    selected_stocks = list(set(selected_stocks))
    selected_stocks = [s for s in selected_stocks if s not in ["MEDIAN", "PRICE", "TOTAL"]]

    print(f"Verifying profitability on {len(selected_stocks)} diverse stocks...")

    results_unleveraged = []
    results_leveraged = []

    # Backtest parameters
    k_atr = 1.5
    rr_ratio = 2.0
    period = "2y"

    for ticker in selected_stocks:
        print(f"Backtesting {ticker}...          ", end="\r")
        try:
            data = yf.download(ticker, period=period, auto_adjust=True, progress=False, timeout=10)
            if data.empty:
                continue

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            # Unleveraged Backtest
            _, metrics_u = run_backtest(data, k_atr=k_atr, rr_ratio=rr_ratio, leverage_mode=False)
            results_unleveraged.append({
                "Ticker": ticker,
                "Return (%)": round(metrics_u["total_return"] * 100, 2),
                "Max DD (%)": round(metrics_u["max_drawdown"] * 100, 2),
                "Profit Factor": round(metrics_u["profit_factor"], 2) if metrics_u["profit_factor"] != np.inf else 10.0,
                "Win Rate (%)": round(metrics_u["win_rate"] * 100, 2),
                "Trades": metrics_u["trade_count"]
            })

            # Leveraged Backtest
            _, metrics_l = run_backtest(data, k_atr=k_atr, rr_ratio=rr_ratio, leverage_mode=True)
            results_leveraged.append({
                "Ticker": ticker,
                "Return (%)": round(metrics_l["total_return"] * 100, 2),
                "Max DD (%)": round(metrics_l["max_drawdown"] * 100, 2),
                "Profit Factor": round(metrics_l["profit_factor"], 2) if metrics_l["profit_factor"] != np.inf else 10.0,
                "Win Rate (%)": round(metrics_l["win_rate"] * 100, 2),
                "Trades": metrics_l["trade_count"]
            })

        except Exception as e:
            print(f"Error backtesting {ticker}: {e}")

    # Aggregate results
    if not results_unleveraged:
        print("No results to aggregate.")
        return None

    df_u = pd.DataFrame(results_unleveraged)
    df_l = pd.DataFrame(results_leveraged)

    summary = {
        "Unleveraged Avg Return (%)": df_u["Return (%)"].mean(),
        "Leveraged Avg Return (%)": df_l["Return (%)"].mean(),
        "Unleveraged Profitable Stocks (%)": (df_u["Return (%)"] > 0).mean() * 100,
        "Leveraged Profitable Stocks (%)": (df_l["Return (%)"] > 0).mean() * 100,
        "Unleveraged Avg Max DD (%)": df_u["Max DD (%)"].mean(),
        "Leveraged Avg Max DD (%)": df_l["Max DD (%)"].mean(),
        "Total Trades (Unleveraged)": df_u["Trades"].sum(),
        "Total Trades (Leveraged)": df_l["Trades"].sum()
    }

    print("\n\n" + "="*40)
    print("BACKTEST COMPARISON: UNLEVERAGED VS LEVERAGED")
    print("="*40)
    for key, val in summary.items():
        print(f"{key}: {val:.2f}")
    print("="*40)

    # Save detailed results to CSV
    df_l.to_csv("backtesting/verification_results_leveraged.csv", index=False)
    print("\nDetailed results saved to backtesting/verification_results_leveraged.csv")

    return summary

if __name__ == "__main__":
    verify_profitability()
