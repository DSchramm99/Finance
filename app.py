import streamlit as st
import pandas as pd

from backtesting.multi_asset import (
    optimize_global_parameters,
    run_global_backtest
)

st.set_page_config(layout="wide")

st.title("📊 Trading Strategy Optimizer")

# ==============================
# Sidebar Settings
# ==============================

st.sidebar.header("Settings")

tickers = st.sidebar.multiselect(
    "Select Tickers",
    [
        "AAPL", "MSFT", "NVDA", "JPM", "JNJ", "PG",
        "SAP.DE", "SIE.DE", "BMW.DE"
    ],
    default=["AAPL", "MSFT", "NVDA"]
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2018-01-01")
)

train_end = st.sidebar.date_input(
    "Train End Date",
    value=pd.to_datetime("2022-12-31")
)

run_button = st.sidebar.button("Run Optimization")

# ==============================
# Parameter Search Space
# ==============================

k_values = [1.0, 1.25, 1.5, 1.75, 2.0]

stop_pct_values = [
    0.03,
    0.05,
    0.07,
    0.10
]

# ==============================
# Run Optimization
# ==============================

if run_button:

    st.subheader("🔎 Optimizing Global Parameters")

    best_params = optimize_global_parameters(
        tickers,
        str(start_date),
        str(train_end),
        k_values,
        stop_pct_values
    )

    st.success("Best Parameters Found")

    st.write(best_params)

    best_k = best_params["k"]
    best_stop = best_params["stop_pct"]

    # ==============================
    # Run Final Backtest
    # ==============================

    st.subheader("📈 Running Test Backtest")

    test_results, portfolio_equity = run_global_backtest(
        tickers,
        str(start_date),
        str(train_end),
        best_k,
        best_stop
    )

    # ==============================
    # Portfolio Equity
    # ==============================

    st.subheader("📊 Portfolio Equity Curve")

    if portfolio_equity is not None:
        st.line_chart(portfolio_equity["Portfolio_Equity"])

    # ==============================
    # Asset Results
    # ==============================

    st.subheader("📋 Asset Performance")

    if test_results:

        df = pd.DataFrame(test_results)

        st.dataframe(df)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Return",
            round(df["total_return"].mean(), 3)
        )

        col2.metric(
            "Average Max Drawdown",
            round(df["max_drawdown"].mean(), 3)
        )

        if "profit_factor" in df.columns:
            col3.metric(
                "Average Profit Factor",
                round(df["profit_factor"].mean(), 3)
            )

    # ==============================
    # Single Asset Analysis
    # ==============================

    if test_results:

        st.subheader("🔍 Single Asset Detail")

        selected_asset = st.selectbox(
            "Choose Asset",
            df["ticker"].tolist()
        )

        asset_row = df[df["ticker"] == selected_asset]

        st.write(asset_row)