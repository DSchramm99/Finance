import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

from universe.universe_loader import get_index_universe
from recommendation.engine import generate_recommendations
from backtesting.multi_asset import run_global_backtest


# =====================================================
# Page Setup
# =====================================================

st.set_page_config(layout="wide")
st.title("📊 Professional Trading System")


# =====================================================
# Settings
# =====================================================

START_DATE = "2020-01-01"
TRAIN_END_DATE = "2023-12-31"

DEFAULT_K = 1.5
DEFAULT_STOP_PCT = 0.05


# =====================================================
# Sidebar - Universe
# =====================================================

st.sidebar.header("Universe")

region = st.sidebar.selectbox("Region", ["USA", "Germany"])

if region == "USA":
    index_choice = st.sidebar.selectbox(
        "Index",
        ["S&P 500", "Nasdaq 100", "Dow Jones"]
    )
else:
    index_choice = st.sidebar.selectbox(
        "Index",
        ["DAX", "TecDAX"]
    )


# =====================================================
# Top 5 Signals
# =====================================================

if st.sidebar.button("🚀 Generate Top 5 Signals"):

    tickers = get_index_universe(index_choice)
    results = generate_recommendations(tickers)

    if results.empty:
        st.warning("No data available.")
    else:

        results["risk_score"] = 100 - results["risk_score"]

        score_cols = ["trend_score", "risk_score", "final_score"]
        results[score_cols] = results[score_cols].round(0).astype(int)

        results = results.sort_values(
            by="final_score",
            ascending=False
        ).head(5)

        st.subheader("🏆 Top 5 Aktien")
        st.dataframe(results, use_container_width=True)


# =====================================================
# Portfolio Backtest
# =====================================================

st.sidebar.header("Backtest")

if st.sidebar.button("📈 Run Portfolio Equity Curve"):

    tickers = get_index_universe(index_choice)

    with st.spinner("Running portfolio backtest..."):

        test_results, portfolio_equity = run_global_backtest(
            tickers=tickers,
            start_date=START_DATE,
            train_end_date=TRAIN_END_DATE,
            k=DEFAULT_K,
            stop_pct=DEFAULT_STOP_PCT
        )

    if portfolio_equity is None or portfolio_equity.empty:
        st.warning("No backtest results available.")
    else:

        # =====================================================
        # Clean Portfolio Equity
        # =====================================================

        strategy_equity = portfolio_equity["Portfolio_Equity"].copy()

        strategy_equity = strategy_equity.replace([np.inf, -np.inf], np.nan)
        strategy_equity = strategy_equity.dropna()

        # remove accidental zeros from aggregation bugs
        strategy_equity = strategy_equity.replace(0, np.nan).ffill()

        strategy_equity = strategy_equity / strategy_equity.iloc[0]

        # =====================================================
        # Benchmark (Buy & Hold) – SAFE VERSION
        # =====================================================

        benchmark = yf.download(
            tickers[0],
            start=START_DATE,
            auto_adjust=True,
            progress=False
        )

        benchmark = benchmark.dropna()

        if not benchmark.empty:

            # Benchmark Returns
            benchmark_returns = benchmark["Close"].pct_change().dropna()

            benchmark_equity = (1 + benchmark_returns).cumprod()

            # Align to strategy index safely
            benchmark_equity = benchmark_equity.reindex(
                strategy_equity.index
            ).ffill()

            # Normalize
            benchmark_equity = benchmark_equity / benchmark_equity.iloc[0]

        # =====================================================
        # Metrics
        # =====================================================

        returns = strategy_equity.pct_change().dropna()

        if returns.std() != 0:
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
        else:
            sharpe = 0

        running_max = strategy_equity.cummax()
        drawdown = (strategy_equity - running_max) / running_max
        max_drawdown = drawdown.min()

        # =====================================================
        # Plot
        # =====================================================

        st.subheader("📊 Portfolio Equity vs Benchmark")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=strategy_equity,
                mode="lines",
                name="Strategy"
            )
        )

        if 'benchmark_equity' in locals():
            fig.add_trace(
                go.Scatter(
                    y=benchmark_equity,
                    mode="lines",
                    name="Buy & Hold",
                    line=dict(dash="dash")
                )
            )

        fig.update_layout(
            template="plotly_white",
            height=600,
            xaxis_title="Time",
            yaxis_title="Normalized Equity (Start = 1)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # =====================================================
        # Metrics Display
        # =====================================================

        st.subheader("📈 Performance Metrics")

        col1, col2 = st.columns(2)

        col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
        col2.metric("Max Drawdown", f"{max_drawdown:.2%}")

        if test_results:
            st.subheader("📋 Test Results")
            st.dataframe(pd.DataFrame(test_results), use_container_width=True)