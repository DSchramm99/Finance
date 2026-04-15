import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

from universe.universe_loader import get_index_universe
from database.db_manager import (
    init_db,
    get_capital,
    set_capital,
    add_trade,
    close_trade,
    get_open_trades,
    reset_database,
    delete_trade,
    get_closed_trades
)

# ============================
# 🔹 Position Manager & Signal Engine
# ============================

from strategy.position_manager import calculate_position_value
from strategy.signal_engine import generate_signal, add_indicators

init_db("TEST", 2000)
init_db("LIVE", 2000)

# =====================================================
# Page Setup
# =====================================================

st.set_page_config(layout="wide")
st.title("📊 Professional Trading System")

# =====================================================
# 🔹 Sidebar Navigation
# =====================================================

if "page" not in st.session_state:
    st.session_state["page"] = "Signals"

st.sidebar.header("Navigation")

if st.sidebar.button("📊 Signals", use_container_width=True):
    st.session_state["page"] = "Signals"

if st.sidebar.button("🧪 Test Portfolio", use_container_width=True):
    st.session_state["page"] = "Test"

if st.sidebar.button("💰 Live Portfolio", use_container_width=True):
    st.session_state["page"] = "Live"

page = st.session_state["page"]

# =====================================================
# 🔹 Aktives Trading Budget
# =====================================================

ACTIVE_BUDGET_TEST = get_capital("TEST") or 2000
ACTIVE_BUDGET_LIVE = get_capital("LIVE") or 2000

# =====================================================
# Sidebar
# =====================================================

if page == "Signals":
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

    # 🔹 Hebel-Modus Toggle
    leverage_mode = st.sidebar.radio("Modus", ["Ohne Hebel", "Gehebelt"], index=0)
    is_leveraged = leverage_mode == "Gehebelt"

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
    # Ticker Analyse
    # =====================================================

    def analyze_ticker(ticker, lev_mode):
        try:
            data = load_price_data(ticker)
            if data.empty: return None

            signal_data = generate_signal(data, leverage_mode=lev_mode)
            if signal_data is None: return None

            return {
                "ticker": ticker,
                "latest_price": signal_data["latest_price"],
                "entry_price": signal_data["entry_price"],
                "stop_level": signal_data["stop_level"],
                "take_profit": signal_data["take_profit"],
                "trend_score": signal_data["trend_score"],
                "risk_score": signal_data["risk_score"],
                "final_score": signal_data["final_score"],
                "signal": signal_data["signal"],
                "leverage": signal_data["leverage"]
            }
        except: return None


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
            result = analyze_ticker(ticker, is_leveraged)
            if result: results.append(result)
            progress_bar.progress((i + 1) / len(tickers))

        status_text.text("Fertig ✅")

        if results:
            df = pd.DataFrame(results)
            df = df.sort_values("final_score", ascending=False).head(5)

            # Investment calculation
            df["Investment (€)"] = df.apply(
                lambda row: calculate_position_value(
                    ACTIVE_BUDGET_TEST if region == "USA" else ACTIVE_BUDGET_TEST,
                    row["risk_score"],
                    row["entry_price"],
                    row["stop_level"]
                ),
                axis=1
            )
            st.session_state["results"] = df


    # =====================================================
    # Display Results
    # =====================================================

    if "results" in st.session_state:
        results = st.session_state["results"]

        company_names = {}
        for ticker in results["ticker"]:
            try:
                company_names[ticker] = yf.Ticker(ticker).info.get("longName", ticker)
            except:
                company_names[ticker] = ticker
        results["company_name"] = results["ticker"].map(company_names)

        st.subheader(f"🏆 Top 5 Aktien ({leverage_mode})")

        # Highlight BUY signals
        def style_signals(row):
            if row.Signal == "BUY":
                return ['background-color: #d4edda; color: #155724'] * len(row)
            return [''] * len(row)

        display_cols = [
            "company_name",
            "signal",
            "leverage",
            "latest_price",
            "entry_price",
            "stop_level",
            "take_profit",
            "trend_score",
            "risk_score",
            "final_score",
            "Investment (€)"
        ]

        display_df = results[display_cols].rename(columns={
            "company_name": "Company",
            "signal": "Signal",
            "leverage": "Leverage",
            "latest_price": "Latest Price",
            "entry_price": "Entry Price",
            "stop_level": "Stop Level",
            "take_profit": "Take Profit",
            "trend_score": "Trend Score",
            "risk_score": "Risk Score",
            "final_score": "Final Score"
        })

        st.dataframe(
            display_df.style.apply(style_signals, axis=1),
            column_config={
                "Trend Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d"),
                "Risk Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d"),
                "Final Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d"),
                "Latest Price": st.column_config.NumberColumn(format="%.2f"),
                "Entry Price": st.column_config.NumberColumn(format="%.2f"),
                "Stop Level": st.column_config.NumberColumn(format="%.2f"),
                "Take Profit": st.column_config.NumberColumn(format="%.2f"),
                "Investment (€)": st.column_config.NumberColumn(format="%.2f"),
                "Leverage": st.column_config.NumberColumn(format="%.1fx")
            },
            use_container_width=True,
            hide_index=True
        )

        # =====================================================
        # Chart
        # =====================================================
        st.subheader("📈 Chart Analyse")
        selected_company = st.selectbox("Aktie auswählen", results["company_name"])
        selected_row = results[results["company_name"] == selected_company].iloc[0]
        selected_ticker = selected_row["ticker"]

        time_period = st.selectbox("Zeitraum", ["1mo", "6mo", "1y"])
        data = load_price_data(selected_ticker)
        data = add_indicators(data)

        if time_period == "1mo": cutoff = pd.Timestamp.today() - pd.Timedelta(days=30)
        elif time_period == "6mo": cutoff = pd.Timestamp.today() - pd.Timedelta(days=182)
        else: cutoff = pd.Timestamp.today() - pd.Timedelta(days=365)
        plot_data = data[data.index >= cutoff]

        y_values = pd.concat([plot_data["Close"], plot_data["SMA20"], plot_data["SMA50"], plot_data["SMA200"]]).dropna()
        if not y_values.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=plot_data.index, y=plot_data["Close"], name="Close"))
            fig.add_trace(go.Scatter(x=plot_data.index, y=plot_data["SMA20"], name="SMA20", line=dict(dash="dash")))
            fig.add_trace(go.Scatter(x=plot_data.index, y=plot_data["SMA50"], name="SMA50", line=dict(dash="dash")))
            fig.add_trace(go.Scatter(x=plot_data.index, y=plot_data["SMA200"], name="SMA200", line=dict(dash="dot")))
            fig.add_hline(y=float(selected_row["entry_price"]), line_dash="dot")
            fig.add_hline(y=float(selected_row["stop_level"]), line_dash="dash")
            fig.add_hline(y=float(selected_row["take_profit"]), line_dash="dash")
            fig.update_layout(template="plotly_white", height=500, title=selected_company)
            st.plotly_chart(fig, use_container_width=True)


    # =====================================================
    # Trade Eröffnung
    # =====================================================
    if "results" in st.session_state:
        st.subheader("📥 Trade eröffnen")
        results = st.session_state["results"]
        selected_company = st.selectbox("Aktie wählen", results["company_name"], key="trade_select_box")
        selected_row = results[results["company_name"] == selected_company].iloc[0]

        with st.form("trade_form"):
            db_mode = st.selectbox("Modus", ["TEST", "LIVE"])
            entry_price = st.number_input("Kaufkurs", value=round(float(selected_row["latest_price"]), 2))
            position_value = st.number_input("Positionsgröße (€)", value=float(selected_row["Investment (€)"]))
            fees = st.number_input("Kaufgebühren (€)", value=0.0)
            leverage = st.number_input("Hebel (Leverage)", value=float(selected_row["leverage"]), min_value=1.0, max_value=10.0, step=0.1)
            submit = st.form_submit_button("Trade bestätigen")

            if submit:
                add_trade(db_mode, selected_row["ticker"], entry_price, selected_row["stop_level"], selected_row["take_profit"], position_value, fees, leverage)
                st.success("Trade gespeichert!")

# =====================================================
# 🧪 / 💰 PORTFOLIO (Unified)
# =====================================================

if page in ["Test", "Live"]:
    mode = "TEST" if page == "Test" else "LIVE"
    st.header("🧪 Test Portfolio" if mode == "TEST" else "💰 Live Portfolio")

    # CAPITAL AND SUMMARY
    capital = get_capital(mode) or 2000
    open_trades_df = get_open_trades(mode)
    closed_trades_df = get_closed_trades(mode)

    invested = 0
    if not open_trades_df.empty:
        invested = open_trades_df["position_value"].sum()

    cash = max(capital - invested, 0)

    # 🔹 Visuals
    col_v1, col_v2 = st.columns([1, 2])

    with col_v1:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Investiert", x=["Kapital"], y=[invested]))
        fig_bar.add_trace(go.Bar(name="Uninvestiert", x=["Kapital"], y=[cash]))
        fig_bar.update_layout(barmode="stack", title="Kapitalverteilung", height=350, template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_v2:
        total_profit_abs = 0
        if not closed_trades_df.empty:
            total_profit_abs = closed_trades_df["profit"].sum()

        profit_pct = (total_profit_abs / capital * 100) if capital > 0 else 0
        color = "green" if total_profit_abs >= 0 else "red"

        st.markdown(f"""
        <div style="text-align: center; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
            <p style="font-size: 20px; margin-bottom: 5px;">Gesamtprofit</p>
            <p style="font-size: 40px; font-weight: bold; color: {color}; margin: 0;">€ {total_profit_abs:,.2f}</p>
            <p style="font-size: 24px; color: {color}; margin: 0;">({profit_pct:,.2f}%)</p>
        </div>
        """, unsafe_allow_html=True)

        if not closed_trades_df.empty:
            closed_trades_df = closed_trades_df.sort_values("timestamp")
            equity_curve = [capital - total_profit_abs]
            for p in closed_trades_df["profit"]:
                equity_curve.append(equity_curve[-1] + p)

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(y=equity_curve, mode='lines+markers', name="Portfolio Wert"))
            fig_line.update_layout(title="Kapitalentwicklung (Abgeschlossene Trades)", height=250, template="plotly_white")
            st.plotly_chart(fig_line, use_container_width=True)

    # REAL TIME MONITORING FOR OPEN TRADES
    if not open_trades_df.empty:
        st.subheader("📡 Real-time Monitoring")

        monitored_data = []
        for _, trade in open_trades_df.iterrows():
            ticker = trade["ticker"]
            try:
                @st.cache_data(ttl=86400)
                def get_company_name(t):
                    try: return yf.Ticker(t).info.get("longName", t)
                    except: return t

                comp_name = get_company_name(ticker)

                start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
                if trade["timestamp"]:
                    start_date = (datetime.strptime(trade["timestamp"], "%Y-%m-%d %H:%M:%S") - timedelta(days=14)).strftime("%Y-%m-%d")

                data = yf.download(ticker, start=start_date, auto_adjust=True, progress=False)
                if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
                data = add_indicators(data)

                if trade["timestamp"]:
                    trade_time = pd.Timestamp(trade["timestamp"])
                    data_since_trade = data[data.index >= trade_time]
                    if data_since_trade.empty: data_since_trade = data.tail(1)
                    highest_price = data_since_trade["High"].max()
                else:
                    highest_price = data["High"].tail(10).max()

                latest = data.iloc[-1]
                price = float(latest["Close"])
                atr = float(latest["ATR"])
                leverage = trade["leverage"] if trade["leverage"] is not None else 1.0

                # Chandelier trailing stop
                effective_k = 1.5 + (max(0, leverage - 1) * 0.5)
                chandelier_stop = highest_price - (effective_k * atr)
                actual_stop = max(trade["stop"], chandelier_stop)
                tp_level = trade["take_profit"]

                action = "HOLD"
                row_color = ""
                # Check liquidation
                if leverage > 1.0 and price <= trade["entry"] * (1 - (1.0 / leverage)):
                    action = "LIQUIDATION"
                    row_color = 'background-color: #f8d7da; color: #721c24'
                elif price <= actual_stop:
                    action = "SELL (STOP)"
                    row_color = 'background-color: #f8d7da; color: #721c24'
                elif price >= tp_level:
                    action = "SELL (TP)"
                    row_color = 'background-color: #d4edda; color: #155724'

                monitored_data.append({
                    "id": trade["id"],
                    "Company": comp_name,
                    "Ticker": ticker,
                    "Price": price,
                    "Entry": trade["entry"],
                    "Profit (%)": ((price / trade["entry"]) - 1) * leverage * 100,
                    "Stop": actual_stop,
                    "Take Profit": tp_level,
                    "Leverage": leverage,
                    "Action": action,
                    "_color": row_color
                })
            except Exception as e:
                st.error(f"Error updating {ticker}: {e}")

        if monitored_data:
            mon_df = pd.DataFrame(monitored_data)
            display_cols = [c for c in mon_df.columns if c != "_color"]
            def style_mon(row): return [row["_color"]] * len(row)

            st.dataframe(
                mon_df.style.apply(style_mon, axis=1).format({
                    "Price": "{:.2f}",
                    "Entry": "{:.2f}",
                    "Profit (%)": "{:.2f}%",
                    "Stop": "{:.2f}",
                    "Take Profit": "{:.2f}",
                    "Leverage": "{:.1f}x"
                }),
                column_order=display_cols,
                use_container_width=True,
                hide_index=True
            )

    # PORTFOLIO MANAGEMENT
    st.divider()
    st.subheader(f"📂 Trades")
    view_mode = st.radio("Ansicht", ["Offene Trades", "Abgeschlossene Trades"], key=f"{mode}_view", horizontal=True)
    df_trades = open_trades_df if view_mode == "Offene Trades" else closed_trades_df

    if df_trades.empty:
        st.info("Keine Trades vorhanden.")
    else:
        num_cols = df_trades.select_dtypes(include=[np.number]).columns.tolist()
        if "id" in num_cols: num_cols.remove("id")

        st.dataframe(
            df_trades.style.format({col: "{:.2f}" for col in num_cols}),
            use_container_width=True
        )

        st.subheader("🛠 Aktionen")
        selected_id = st.selectbox("Trade ID auswählen", df_trades["id"], key=f"{mode}_id_select")

        col1, col2, col3 = st.columns(3)
        with col1:
            if view_mode == "Offene Trades":
                st.write("Trade schließen:")
                exit_price = st.number_input("Exit Preis", key=f"{mode}_exit_val")
                fee = st.number_input("Verkaufsgebühr", value=0.0, key=f"{mode}_fee_val")
                if st.button("Close Trade", key=f"{mode}_close_btn_act"):
                    close_trade(mode, selected_id, exit_price, fee)
                    st.rerun()
        with col2:
            st.write("Trade löschen:")
            if st.button("🗑 Delete Single Trade", key=f"{mode}_delete_btn", help="This action cannot be undone."):
                delete_trade(mode, selected_id)
                st.rerun()

    if mode == "TEST":
        st.divider()
        st.subheader("⚠️ Database Maintenance")
        if st.button("🔥 RESET ENTIRE TEST DATABASE", use_container_width=True, help="All data in the test portfolio will be permanently deleted."):
            reset_database("TEST", 2000)
            st.success("Database Reset successful!")
            st.rerun()
