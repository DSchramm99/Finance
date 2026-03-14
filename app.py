import streamlit as st
import pandas as pd

from universe.universe_loader import get_index_universe
from recommendation.engine import generate_recommendations

from backtesting.multi_asset import (
    optimize_global_parameters,
    run_global_backtest
)

# =====================================================
# Page Setup
# =====================================================

st.set_page_config(layout="wide")
st.title("📊 Trading System")


# =====================================================
# Region -> Index Kopplung (keine ungültigen Kombinationen)
# =====================================================

region = st.sidebar.selectbox(
    "Region",
    ["USA", "Germany"]
)

if region == "USA":
    index_choice = st.sidebar.selectbox(
        "Index",
        ["S&P 500", "Nasdaq 100", "Dow Jones"]
    )

elif region == "Germany":
    index_choice = st.sidebar.selectbox(
        "Index",
        ["DAX", "TecDAX"]
    )


# =====================================================
# Recommendation Button
# =====================================================

run_scan = st.sidebar.button("🔎 Run Recommendations")


# =====================================================
# Backtest Settings
# =====================================================

st.sidebar.header("Backtest (Optional)")

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2018-01-01")
)

train_end = st.sidebar.date_input(
    "Train End Date",
    value=pd.to_datetime("2022-12-31")
)

run_backtest = st.sidebar.button("📈 Run Optimization")


# =====================================================
# Recommendation Engine
# =====================================================

if run_scan:

    tickers = get_index_universe(index_choice)

    st.write(f"{len(tickers)} tickers loaded")

    if not tickers:
        st.error("No tickers available.")
        st.stop()

    results = generate_recommendations(
        tickers,
        k=1.5,
        drawdown_limit=0.2
    )

    if results.empty:
        st.warning("No signals found.")
    else:
        st.subheader("🏆 Top 5 Recommendations")
        st.dataframe(results.head(5))


# =====================================================
# Backtest Section
# =====================================================

if run_backtest:

    tickers = get_index_universe(index_choice)

    k_values = [1.0, 1.25, 1.5, 1.75, 2.0]
    stop_pct_values = [0.03, 0.05, 0.07, 0.10]

    best_params = optimize_global_parameters(
        tickers,
        str(start_date),
        str(train_end),
        k_values,
        stop_pct_values
    )

    if best_params is None:
        st.error("No valid parameters found.")
        st.stop()

    st.write(best_params)

    best_k = best_params["k"]
    best_stop = best_params["stop_pct"]

    test_results, portfolio_equity = run_global_backtest(
        tickers,
        str(start_date),
        str(train_end),
        best_k,
        best_stop
    )

    if portfolio_equity is not None:
        st.line_chart(portfolio_equity["Portfolio_Equity"])

    if test_results:
        st.dataframe(pd.DataFrame(test_results))