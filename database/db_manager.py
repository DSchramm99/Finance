import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import streamlit as st

# =====================================================
# Database Selector
# =====================================================

# Support for SQLAlchemy (PostgreSQL/MySQL/etc via DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")
_ENGINE = None

# Support for Supabase API (via SUPABASE_URL and SUPABASE_KEY)
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
except Exception:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_SUPABASE_CLIENT = None

def get_supabase():
    global _SUPABASE_CLIENT
    if _SUPABASE_CLIENT is None and SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        _SUPABASE_CLIENT = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _SUPABASE_CLIENT

def get_engine():
    global _ENGINE
    if _ENGINE is None and DATABASE_URL:
        _ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _ENGINE

def get_connection(mode):
    engine = get_engine()
    if engine:
        return engine.connect()
    else:
        # SQLite fallback
        import sqlite3
        db_path = "trading_test.db" if mode == "TEST" else "trading_live.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

# =====================================================
# Initialize Database
# =====================================================

def init_db(mode, start_capital=2000):
    supabase = get_supabase()
    if supabase:
        # Supabase tables should be created via SQL Editor in dashboard
        # But we check if portfolio exists
        try:
            res = supabase.table("portfolio").select("*").eq("trade_mode", mode).execute()
            if not res.data:
                supabase.table("portfolio").insert({"capital": start_capital, "trade_mode": mode}).execute()
        except Exception as e:
            st.warning(f"Supabase Init: {e}. Please ensure 'portfolio' and 'trades' tables are created in Supabase.")
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        queries = [
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id SERIAL PRIMARY KEY,
                capital DOUBLE PRECISION,
                trade_mode TEXT UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS trades (
                id SERIAL PRIMARY KEY,
                ticker TEXT,
                entry DOUBLE PRECISION,
                stop DOUBLE PRECISION,
                take_profit DOUBLE PRECISION,
                exit_price DOUBLE PRECISION,
                position_value DOUBLE PRECISION,
                fees DOUBLE PRECISION,
                profit DOUBLE PRECISION,
                status TEXT,
                timestamp TEXT,
                leverage DOUBLE PRECISION,
                trade_mode TEXT
            )
            """
        ]
        for q in queries:
            conn.execute(text(q))

        res = conn.execute(text("SELECT * FROM portfolio WHERE trade_mode=:mode"), {"mode": mode}).fetchone()
        if res is None:
            conn.execute(text("INSERT INTO portfolio (capital, trade_mode) VALUES (:cap, :mode)"), {"cap": start_capital, "mode": mode})

        conn.commit()
        conn.close()
    else:
        # SQLite syntax
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS portfolio (id INTEGER PRIMARY KEY, capital REAL)")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT, entry REAL, stop REAL, take_profit REAL, exit_price REAL,
                position_value REAL, fees REAL, profit REAL, status TEXT, timestamp TEXT, leverage REAL
            )
        """)
        cursor.execute("PRAGMA table_info(trades)")
        columns = [col[1] for col in cursor.fetchall()]
        if "timestamp" not in columns: cursor.execute("ALTER TABLE trades ADD COLUMN timestamp TEXT")
        if "leverage" not in columns: cursor.execute("ALTER TABLE trades ADD COLUMN leverage REAL DEFAULT 1.0")
        cursor.execute("SELECT * FROM portfolio WHERE id=1")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO portfolio (id, capital) VALUES (1, ?)", (start_capital,))
        conn.commit()
        conn.close()


# =====================================================
# Capital Functions
# =====================================================

def get_capital(mode="TEST"):
    supabase = get_supabase()
    if supabase:
        res = supabase.table("portfolio").select("capital").eq("trade_mode", mode).execute()
        return res.data[0]["capital"] if res.data else None

    conn = get_connection(mode)
    if DATABASE_URL:
        row = conn.execute(text("SELECT capital FROM portfolio WHERE trade_mode=:mode"), {"mode": mode}).fetchone()
        capital = row[0] if row else None
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT capital FROM portfolio WHERE id=1")
        row = cursor.fetchone()
        capital = row[0] if row else None
    conn.close()
    return capital


def set_capital(amount, mode="TEST"):
    supabase = get_supabase()
    if supabase:
        supabase.table("portfolio").update({"capital": amount}).eq("trade_mode", mode).execute()
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("UPDATE portfolio SET capital=:amount WHERE trade_mode=:mode"), {"amount": amount, "mode": mode})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("UPDATE portfolio SET capital = ? WHERE id=1", (amount,))
        conn.commit()
    conn.close()


# =====================================================
# Trade Functions
# =====================================================

def add_trade(mode, ticker, entry, stop, tp, position_value, fees, leverage=1.0):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    supabase = get_supabase()
    if supabase:
        supabase.table("trades").insert({
            "ticker": ticker, "entry": entry, "stop": stop, "take_profit": tp,
            "position_value": position_value, "fees": fees, "status": "OPEN",
            "timestamp": timestamp, "leverage": leverage, "trade_mode": mode
        }).execute()
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("""
            INSERT INTO trades
            (ticker, entry, stop, take_profit, position_value, fees, status, timestamp, leverage, trade_mode)
            VALUES (:ticker, :entry, :stop, :tp, :pos, :fees, 'OPEN', :ts, :lev, :mode)
        """), {
            "ticker": ticker, "entry": entry, "stop": stop, "tp": tp,
            "pos": position_value, "fees": fees, "ts": timestamp, "lev": leverage, "mode": mode
        })
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trades
            (ticker, entry, stop, take_profit, position_value, fees, status, timestamp, leverage)
            VALUES (?, ?, ?, ?, ?, ?, 'OPEN', ?, ?)
        """, (ticker, entry, stop, tp, position_value, fees, timestamp, leverage))
        conn.commit()
    conn.close()

def close_trade(mode, trade_id, exit_price, sell_fee = 0):
    supabase = get_supabase()
    if supabase:
        res = supabase.table("trades").select("*").eq("id", trade_id).execute()
        if not res.data: return
        trade = res.data[0]
        entry, position_value, fees, leverage = trade["entry"], trade["position_value"], trade["fees"], trade.get("leverage", 1.0) or 1.0
        profit = ((exit_price - entry) * (position_value / entry) * leverage) - sell_fee - fees
        supabase.table("trades").update({"exit_price": exit_price, "profit": profit, "status": "CLOSED"}).eq("id", trade_id).execute()
        cap_res = supabase.table("portfolio").select("capital").eq("trade_mode", mode).execute()
        if cap_res.data:
            supabase.table("portfolio").update({"capital": cap_res.data[0]["capital"] + profit}).eq("trade_mode", mode).execute()
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        trade = conn.execute(text("SELECT * FROM trades WHERE id = :id"), {"id": trade_id}).fetchone()
        if not trade:
            conn.close()
            return
        t = trade._mapping
        profit = ((exit_price - t["entry"]) * (t["position_value"] / t["entry"]) * (t["leverage"] or 1.0)) - sell_fee - t["fees"]
        conn.execute(text("UPDATE trades SET exit_price=:exit, profit=:profit, status='CLOSED' WHERE id=:id"), {"exit": exit_price, "profit": profit, "id": trade_id})
        row = conn.execute(text("SELECT capital FROM portfolio WHERE trade_mode=:mode"), {"mode": mode}).fetchone()
        if row: conn.execute(text("UPDATE portfolio SET capital = :cap WHERE trade_mode=:mode"), {"cap": row[0] + profit, "mode": mode})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
        trade = cursor.fetchone()
        if not trade:
            conn.close()
            return
        profit = ((exit_price - trade["entry"]) * (trade["position_value"] / trade["entry"]) * (trade["leverage"] or 1.0)) - sell_fee - trade["fees"]
        cursor.execute("UPDATE trades SET exit_price=?, profit=?, status='CLOSED' WHERE id=?", (exit_price, profit, trade_id))
        cursor.execute("SELECT capital FROM portfolio WHERE id=1")
        row = cursor.fetchone()
        if row: cursor.execute("UPDATE portfolio SET capital = ? WHERE id=1", (row["capital"] + profit,))
        conn.commit()
    conn.close()

def get_open_trades(mode):
    supabase = get_supabase()
    if supabase:
        res = supabase.table("trades").select("*").eq("status", "OPEN").eq("trade_mode", mode).execute()
        return pd.DataFrame(res.data)

    conn = get_connection(mode)
    if DATABASE_URL:
        df = pd.read_sql_query(text("SELECT * FROM trades WHERE status='OPEN' AND trade_mode=:mode"), conn, params={"mode": mode})
    else:
        df = pd.read_sql_query("SELECT * FROM trades WHERE status='OPEN'", conn)
    conn.close()
    return df

def delete_trade(mode, trade_id):
    supabase = get_supabase()
    if supabase:
        supabase.table("trades").delete().eq("id", trade_id).execute()
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("DELETE FROM trades WHERE id=:id"), {"id": trade_id})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trades WHERE id=?", (trade_id,))
        conn.commit()
    conn.close()


def update_trade_exit(mode, trade_id, exit_price):
    supabase = get_supabase()
    if supabase:
        supabase.table("trades").update({"exit_price": exit_price, "status": "CLOSED"}).eq("id", trade_id).execute()
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("UPDATE trades SET exit_price=:exit, status='CLOSED' WHERE id=:id"), {"exit": exit_price, "id": trade_id})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("UPDATE trades SET exit_price=?, status='CLOSED' WHERE id=?", (exit_price, trade_id))
        conn.commit()
    conn.close()

def get_closed_trades(mode):
    supabase = get_supabase()
    if supabase:
        res = supabase.table("trades").select("*").eq("status", "CLOSED").eq("trade_mode", mode).execute()
        return pd.DataFrame(res.data)

    conn = get_connection(mode)
    if DATABASE_URL:
        df = pd.read_sql_query(text("SELECT * FROM trades WHERE status='CLOSED' AND trade_mode=:mode"), conn, params={"mode": mode})
    else:
        df = pd.read_sql("SELECT * FROM trades WHERE status='CLOSED'", conn)
    conn.close()
    return df

def reset_database(mode, start_capital):
    supabase = get_supabase()
    if supabase:
        supabase.table("trades").delete().eq("trade_mode", mode).execute()
        supabase.table("portfolio").update({"capital": start_capital}).eq("trade_mode", mode).execute()
        return

    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("DELETE FROM trades WHERE trade_mode=:mode"), {"mode": mode})
        conn.execute(text("UPDATE portfolio SET capital = :cap WHERE trade_mode = :mode"), {"cap": start_capital, "mode": mode})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trades")
        cursor.execute("UPDATE portfolio SET capital = ? WHERE id = 1", (start_capital,))
        conn.commit()
    conn.close()
