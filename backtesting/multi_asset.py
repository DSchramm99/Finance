import yfinance as yf
import pandas as pd
import numpy as np

from .optimizer import (
    train_test_split,
    run_backtest
)


# ==============================
# Global Optimization
# ==============================

def optimize_global_parameters(
    tickers,
    start_date,
    train_end_date,
    k_values,
    stop_percent_values
):

    best_score = -np.inf
    best_params = None

    for k in k_values:
        for stop_pct in stop_percent_values:

            portfolio_returns = []

            for ticker in tickers:

                data = yf.download(ticker, start=start_date, auto_adjust=True)

                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                data = data.dropna()

                train, _ = train_test_split(data, train_end_date)

                if len(train) < 250:
                    continue

                _, metrics = run_backtest(
                    train,
                    k_atr=k,
                    fixed_stop_pct=stop_pct
                )

                portfolio_returns.append(metrics["total_return"])

            if len(portfolio_returns) == 0:
                continue

            # Simple global score
            avg_return = np.mean(portfolio_returns)

            # Drawdown penalty optional (wenn vorhanden)
            score = avg_return

            if score > best_score:
                best_score = score
                best_params = {
                    "k": k,
                    "stop_pct": stop_pct
                }

    return best_params


# ==============================
# Final Evaluation (Test Set)
# ==============================

def run_global_backtest(
    tickers,
    start_date,
    train_end_date,
    k,
    stop_pct
):

    all_test_results = []
    portfolio_equity = None

    for ticker in tickers:

        data = yf.download(ticker, start=start_date)
        data = data.dropna()

        train, test = train_test_split(data, train_end_date)

        if len(test) < 50:
            continue

        _, train_metrics = run_backtest(
            train,
            k_atr=k,
            fixed_stop_pct=stop_pct
        )

        equity_curve, test_metrics = run_backtest(
            test,
            k_atr=k,
            fixed_stop_pct=stop_pct,
            return_equity=True
        )

        all_test_results.append({
            "ticker": ticker,
            "k": k,
            "stop_pct": stop_pct,
            **test_metrics
        })

        if portfolio_equity is None:
            portfolio_equity = equity_curve
        else:
            portfolio_equity["Portfolio_Equity"] += equity_curve["Portfolio_Equity"]

    return all_test_results, portfolio_equity