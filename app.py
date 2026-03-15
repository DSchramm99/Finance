import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor, as_completed

from universe.universe_loader import get_index_universe

# =====================================================
# Page Setup
# =====================================================

st.set_page_config(layout="wide")
st.title("📊 Professional Trading System")

# =====================================================
# Sidebar
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
# Cached Price Data
# =====================================================

@st.cache_data(ttl=3600)
def load_price_data(ticker):

    data = yf.download(
        ticker,
        period="2y",
        auto_adjust=True,
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


# =====================================================
# Ticker Analyse (deterministisch)
# =====================================================

def analyze_ticker(ticker):

    try:
        data = load_price_data(ticker)

        if data.empty:
            return None

        data["SMA20"] = data["Close"].rolling(20).mean()
        data["SMA50"] = data["Close"].rolling(50).mean()
        data["SMA200"] = data["Close"].rolling(200).mean()
        data["ATR"] = (data["High"] - data["Low"]).rolling(14).mean()

        latest = data.iloc[-1]

        if pd.isna(latest["SMA20"]) or pd.isna(latest["ATR"]):
            return None

        close = float(latest["Close"])
        sma = float(latest["SMA20"])
        atr = float(latest["ATR"])

        trend_raw = (close - sma) / sma
        trend_score = int(np.clip(50 + trend_raw * 200, 0, 100))

        volatility = atr / close
        risk_score = int(np.clip(100 - (volatility * 500), 0, 100))

        final_score = int(0.6 * trend_score + 0.4 * risk_score)

        entry = close if trend_score > 65 else sma
        stop = entry - (1.5 * atr)
        take_profit = entry + 2 * (entry - stop)

        return {
            "ticker": ticker,
            "latest_price": close,
            "entry_price": entry,
            "stop_level": stop,
            "take_profit": take_profit,
            "trend_score": trend_score,
            "risk_score": risk_score,
            "final_score": final_score
        }

    except:
        return None


# =====================================================
# Generate Signals
# =====================================================

if st.sidebar.button("🚀 Generate Top 5 Signals"):

    tickers = get_index_universe(index_choice)

    progress_bar = st.progress(0)
    status_text = st.empty()

    results = []

    for i, ticker in enumerate(tickers):

        status_text.text(f"Lade & analysiere: {ticker} ({i+1}/{len(tickers)})")

        result = analyze_ticker(ticker)

        if result:
            results.append(result)

        progress_bar.progress((i + 1) / len(tickers))

    status_text.text("Fertig ✅")

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values("final_score", ascending=False).head(5)
        st.session_state["results"] = df


# =====================================================
# Display Results
# =====================================================

if "results" in st.session_state:

    results = st.session_state["results"]

    # Risk invertieren (nur Anzeige)
    results["risk_score"] = 100 - results["risk_score"]

    # Firmenname hinzufügen
    company_names = {}
    for ticker in results["ticker"]:
        try:
            company_names[ticker] = yf.Ticker(ticker).info.get("longName", ticker)
        except:
            company_names[ticker] = ticker

    results["company_name"] = results["ticker"].map(company_names)

    st.subheader("🏆 Top 5 Aktien")

    display_cols = [
        "company_name",
        "latest_price",
        "entry_price",
        "stop_level",
        "take_profit",
        "trend_score",
        "risk_score",
        "final_score"
    ]

    display_df = results[display_cols].rename(columns={
        "company_name": "Company",
        "latest_price": "Latest Price",
        "entry_price": "Entry Price",
        "stop_level": "Stop Level",
        "take_profit": "Take Profit",
        "trend_score": "Trend Score",
        "risk_score": "Risk Score",
        "final_score": "Final Score"
    })

    st.dataframe(
        display_df.round(2),
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Chart
    # =====================================================

    st.subheader("📈 Chart Analyse")

    selected_company = st.selectbox(
        "Aktie auswählen",
        results["company_name"]
    )

    selected_row = results[
        results["company_name"] == selected_company
    ].iloc[0]

    selected_ticker = selected_row["ticker"]

    time_period = st.selectbox(
        "Zeitraum",
        ["1mo", "6mo", "1y"],
        format_func=lambda x: {
            "1mo": "1 Monat",
            "6mo": "6 Monate",
            "1y": "1 Jahr"
        }[x]
    )

    data = load_price_data(selected_ticker)

    data["SMA20"] = data["Close"].rolling(20).mean()
    data["SMA50"] = data["Close"].rolling(50).mean()
    data["SMA200"] = data["Close"].rolling(200).mean()

    # echtes Rolling Window statt pandas .last("1Y")

    if time_period == "1mo":
        cutoff = pd.Timestamp.today() - pd.Timedelta(days=30)
        plot_data = data[data.index >= cutoff]

    elif time_period == "6mo":
        cutoff = pd.Timestamp.today() - pd.Timedelta(days=182)
        plot_data = data[data.index >= cutoff]

    else:  # 1 year
        cutoff = pd.Timestamp.today() - pd.Timedelta(days=365)
        plot_data = data[data.index >= cutoff]

    y_values = pd.concat([
        plot_data["Close"],
        plot_data["SMA20"],
        plot_data["SMA50"],
        plot_data["SMA200"]
    ]).dropna()

    if y_values.empty:
        st.stop()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=plot_data.index,
        y=plot_data["Close"],
        name="Close",
        line=dict(width=2)
    ))

    fig.add_trace(go.Scatter(
        x=plot_data.index,
        y=plot_data["SMA20"],
        name="SMA20",
        line=dict(width=2, dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=plot_data.index,
        y=plot_data["SMA50"],
        name="SMA50",
        line=dict(width=2, dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=plot_data.index,
        y=plot_data["SMA200"],
        name="SMA200",
        line=dict(width=2, dash="dot")
    ))

    fig.add_hline(y=float(selected_row["entry_price"]), line_dash="dot")
    fig.add_hline(y=float(selected_row["stop_level"]), line_dash="dash")
    fig.add_hline(y=float(selected_row["take_profit"]), line_dash="dash")

    fig.update_yaxes(
        range=[
            y_values.min() * 0.95,
            y_values.max() * 1.05
        ]
    )

    fig.update_layout(
        template="plotly_white",
        height=650,
        title=selected_company,
        xaxis_title="Zeit",
        yaxis_title="Preis"
    )

    st.plotly_chart(fig, use_container_width=True)