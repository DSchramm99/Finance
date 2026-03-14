import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Trading Recommendation Tool",
    layout="wide"
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("Settings")

market = st.sidebar.selectbox(
    "Market",
    ["USA", "Germany"]
)

index_options = {
    "USA": ["S&P 500", "NASDAQ"],
    "Germany": ["DAX", "TecDAX"]
}

index = st.sidebar.selectbox(
    "Index",
    index_options[market]
)

# For now: manual ticker input (we can auto-map later)
ticker = st.sidebar.text_input("Ticker Symbol", "AAPL")

timeframe = st.sidebar.selectbox(
    "Timeframe (Short/Mid Term)",
    ["1D", "5D", "1W", "1M", "3M", "6M"]
)

analyze = st.sidebar.button("Run Analysis")

# -------------------------
# Timeframe Mapping
# -------------------------
timeframe_map = {
    "1D": "1d",
    "5D": "5d",
    "1W": "1wk",
    "1M": "1mo",
    "3M": "3mo",
    "6M": "6mo"
}

# -------------------------
# Main Layout
# -------------------------
st.title("📊 Short / Mid-Term Trading Dashboard")

if analyze:

    with st.spinner("Loading data..."):

        data = yf.download(
            ticker,
            period=timeframe_map[timeframe],
            interval="1d"
        )

    if data.empty:
        st.error("No data found for this ticker.")
    else:
        # -------------------------
        # Plotly Chart
        # -------------------------
        fig = go.Figure()

        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Price"
            )
        )

        fig.update_layout(
            height=600,
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------
        # Placeholder Sections
        # -------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Trend Status")
            st.info("Coming soon")

        with col2:
            st.subheader("Risk Score")
            st.info("Coming soon")

        with col3:
            st.subheader("Recommendation")
            st.info("Coming soon")

        st.subheader("Explanation")
        st.write("Analysis logic will appear here.")