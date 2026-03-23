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
                # Clean up tickers (some might have names or extra info)
                # For Dow Jones and TecDAX local CSVs, the loader might need help

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

    # Remove duplicates
    selected_stocks = list(set(selected_stocks))
    # Filter out known bad ones from previous run if any
    selected_stocks = [s for s in selected_stocks if s not in ["MEDIAN", "PRICE", "TOTAL"]]

    print(f"Verifying profitability on {len(selected_stocks)} diverse stocks...")

    all_results = []

    # Backtest parameters
    k_atr = 1.5
    rr_ratio = 2.0
    period = "2y"

    for ticker in selected_stocks:
        print(f"Backtesting {ticker}...          ", end="\r")
        try:
            data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
            if data.empty:
                continue

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            _, metrics = run_backtest(data, k_atr=k_atr, rr_ratio=rr_ratio)

            all_results.append({
                "Ticker": ticker,
                "Return (%)": round(metrics["total_return"] * 100, 2),
                "Max DD (%)": round(metrics["max_drawdown"] * 100, 2),
                "Profit Factor": round(metrics["profit_factor"], 2) if metrics["profit_factor"] != np.inf else 10.0,
                "Win Rate (%)": round(metrics["win_rate"] * 100, 2),
                "Trades": metrics["trade_count"]
            })
        except Exception as e:
            print(f"Error backtesting {ticker}: {e}")

    # Aggregate results
    if not all_results:
        print("No results to aggregate.")
        return None

    results_df = pd.DataFrame(all_results)

    summary = {
        "Avg Return (%)": results_df["Return (%)"].mean(),
        "Median Return (%)": results_df["Return (%)"].median(),
        "Avg Max DD (%)": results_df["Max DD (%)"].mean(),
        "Avg Profit Factor": results_df["Profit Factor"].mean(),
        "Avg Win Rate (%)": results_df["Win Rate (%)"].mean(),
        "Total Trades": results_df["Trades"].sum(),
        "Profitable Stocks (%)": (results_df["Return (%)"] > 0).mean() * 100
    }

    print("\n\n" + "="*30)
    print("BACKTEST SUMMARY")
    print("="*30)
    for key, val in summary.items():
        print(f"{key}: {val:.2f}")
    print("="*30)

    # Save detailed results to CSV
    results_df.to_csv("backtesting/verification_results.csv", index=False)
    print("\nDetailed results saved to backtesting/verification_results.csv")

    return summary

if __name__ == "__main__":
    verify_profitability()
