import pandas as pd
import numpy as np
import yfinance as yf

from .engine import run_backtest
from .optimizer import train_test_split


# =====================================================
# Single Split Evaluation
# =====================================================

def evaluate_split(
    tickers,
    start_date,
    train_end_date,
    k,
    fixed_stop_pct
):

    strategy_equity = None
    benchmark_equity = None

    for ticker in tickers:

        data = yf.download(
            ticker,
            start=start_date,
            auto_adjust=True,
            progress=False
        ).dropna()

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        train, test = train_test_split(data, train_end_date)

        if len(test) < 50:
            continue

        # -------------------------
        # Strategy on Test
        # -------------------------

        equity_curve, _ = run_backtest(
            test,
            k_atr=k,
            fixed_stop_pct=fixed_stop_pct,
            return_equity=True
        )

        if strategy_equity is None:
            strategy_equity = equity_curve.copy()
        else:
            equity_curve = equity_curve.reindex(strategy_equity.index).ffill()
            strategy_equity = strategy_equity.add(equity_curve, fill_value=0)

        # -------------------------
        # Buy & Hold Benchmark
        # -------------------------

        returns = test["Close"].pct_change().dropna()
        bh_equity = (1 + returns).cumprod()

        bh_equity = bh_equity.reindex(strategy_equity.index).ffill()

        if benchmark_equity is None:
            benchmark_equity = bh_equity.copy()
        else:
            benchmark_equity = benchmark_equity.add(bh_equity, fill_value=0)

    return strategy_equity, benchmark_equity


# =====================================================
# Metrics
# =====================================================

def calculate_metrics(equity_series):

    returns = equity_series.pct_change().dropna()

    total_return = equity_series.iloc[-1] - 1

    sharpe = (
        returns.mean() / returns.std()
        * np.sqrt(252)
        if returns.std() != 0 else 0
    )

    running_max = equity_series.cummax()
    drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min()

    return {
        "total_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown
    }


# =====================================================
# Multi Split Runner
# =====================================================

def run_split_benchmark(
    tickers,
    splits,
    start_date,
    k,
    fixed_stop_pct
):

    results = []

    for train_end_date in splits:

        strategy_eq, benchmark_eq = evaluate_split(
            tickers,
            start_date,
            train_end_date,
            k,
            fixed_stop_pct
        )

        if strategy_eq is None:
            continue

        strategy_metrics = calculate_metrics(strategy_eq)
        benchmark_metrics = calculate_metrics(benchmark_eq)

        results.append({
            "train_end": train_end_date,
            "strategy_return": strategy_metrics["total_return"],
            "strategy_sharpe": strategy_metrics["sharpe"],
            "strategy_max_dd": strategy_metrics["max_drawdown"],
            "benchmark_return": benchmark_metrics["total_return"],
            "benchmark_sharpe": benchmark_metrics["sharpe"],
            "benchmark_max_dd": benchmark_metrics["max_drawdown"],
        })

    return pd.DataFrame(results)