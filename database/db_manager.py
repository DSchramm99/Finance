import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

# =====================================================
# Database Selector
# =====================================================

# Get database URL from environment variable (e.g., for PostgreSQL in Cloud)
# Fallback to local SQLite if not provided
DATABASE_URL = os.getenv("DATABASE_URL")
_ENGINE = None

def get_engine():
    global _ENGINE
    if _ENGINE is None and DATABASE_URL:
        _ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _ENGINE

def get_connection(mode):
    engine = get_engine()
    if engine:
        # PostgreSQL, MySQL, etc.
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
    conn = get_connection(mode)

    if DATABASE_URL:
        # PostgreSQL syntax
        # We use a single database but distinguish by a 'mode' column
        queries = [
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id SERIAL PRIMARY KEY,
                capital DOUBLE PRECISION,
                mode TEXT UNIQUE
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
                mode TEXT
            )
            """
        ]
        for q in queries:
            conn.execute(text(q))

        # Check if portfolio needs initialization for this mode
        res = conn.execute(text("SELECT * FROM portfolio WHERE mode=:mode"), {"mode": mode}).fetchone()
        if res is None:
            conn.execute(text("INSERT INTO portfolio (capital, mode) VALUES (:cap, :mode)"), {"cap": start_capital, "mode": mode})

        conn.commit()
    else:
        # SQLite syntax
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY,
                capital REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                entry REAL,
                stop REAL,
                take_profit REAL,
                exit_price REAL,
                position_value REAL,
                fees REAL,
                profit REAL,
                status TEXT,
                timestamp TEXT,
                leverage REAL
            )
        """)

        # Migration: check if columns exist
        cursor.execute("PRAGMA table_info(trades)")
        columns = [col[1] for col in cursor.fetchall()]

        if "timestamp" not in columns:
            cursor.execute("ALTER TABLE trades ADD COLUMN timestamp TEXT")

        if "leverage" not in columns:
            cursor.execute("ALTER TABLE trades ADD COLUMN leverage REAL DEFAULT 1.0")

        cursor.execute("SELECT * FROM portfolio WHERE id=1")
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO portfolio (id, capital) VALUES (1, ?)",
                (start_capital,)
            )

        conn.commit()

    conn.close()


# =====================================================
# Capital Functions
# =====================================================

def get_capital(mode="TEST"):
    conn = get_connection(mode)
    if DATABASE_URL:
        row = conn.execute(text("SELECT capital FROM portfolio WHERE mode=:mode"), {"mode": mode}).fetchone()
        capital = row[0] if row else None
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT capital FROM portfolio WHERE id=1")
        row = cursor.fetchone()
        capital = row[0] if row else None
    conn.close()
    return capital


def set_capital(amount, mode="TEST"):
    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("UPDATE portfolio SET capital=:amount WHERE mode=:mode"), {"amount": amount, "mode": mode})
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
    conn = get_connection(mode)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if DATABASE_URL:
        conn.execute(text("""
            INSERT INTO trades
            (ticker, entry, stop, take_profit, position_value, fees, status, timestamp, leverage, mode)
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
    conn = get_connection(mode)

    if DATABASE_URL:
        trade = conn.execute(text("SELECT * FROM trades WHERE id = :id"), {"id": trade_id}).fetchone()
        if not trade:
            conn.close()
            return

        t = trade._mapping
        entry = t["entry"]
        position_value = t["position_value"]
        fees = t["fees"]
        leverage = t["leverage"] if t["leverage"] is not None else 1.0

        quantity = position_value / entry
        gross_profit = (exit_price - entry) * quantity * leverage
        profit = gross_profit - sell_fee - fees

        conn.execute(text("""
            UPDATE trades
            SET exit_price = :exit,
                profit = :profit,
                status = 'CLOSED'
            WHERE id = :id
        """), {"exit": exit_price, "profit": profit, "id": trade_id})

        row = conn.execute(text("SELECT capital FROM portfolio WHERE mode=:mode"), {"mode": mode}).fetchone()
        if row:
            capital = row[0]
            new_capital = capital + profit
            conn.execute(text("UPDATE portfolio SET capital = :cap WHERE mode=:mode"), {"cap": new_capital, "mode": mode})

        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
        trade = cursor.fetchone()

        if not trade:
            conn.close()
            return

        entry = trade["entry"]
        position_value = trade["position_value"]
        fees = trade["fees"]
        leverage = trade["leverage"] if trade["leverage"] is not None else 1.0

        quantity = position_value / entry
        gross_profit = (exit_price - entry) * quantity * leverage
        profit = gross_profit - sell_fee - fees

        cursor.execute("""
            UPDATE trades
            SET exit_price = ?,
                profit = ?,
                status = 'CLOSED'
            WHERE id = ?
        """, (exit_price, profit, trade_id))

        cursor.execute("SELECT capital FROM portfolio WHERE id=1")
        row = cursor.fetchone()
        if row:
            capital = row["capital"]
            new_capital = capital + profit
            cursor.execute("UPDATE portfolio SET capital = ? WHERE id=1", (new_capital,))

        conn.commit()
    conn.close()

def get_open_trades(mode):
    conn = get_connection(mode)
    if DATABASE_URL:
        df = pd.read_sql_query(text("SELECT * FROM trades WHERE status='OPEN' AND mode=:mode"), conn, params={"mode": mode})
    else:
        df = pd.read_sql_query("SELECT * FROM trades WHERE status='OPEN'", conn)
    conn.close()
    return df

def delete_trade(mode, trade_id):
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
    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("""
            UPDATE trades
            SET exit_price=:exit, status='CLOSED'
            WHERE id=:id
        """), {"exit": exit_price, "id": trade_id})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE trades
            SET exit_price=?, status='CLOSED'
            WHERE id=?
        """, (exit_price, trade_id))
        conn.commit()
    conn.close()

def get_closed_trades(mode):
    conn = get_connection(mode)
    if DATABASE_URL:
        df = pd.read_sql_query(text("SELECT * FROM trades WHERE status='CLOSED' AND mode=:mode"), conn, params={"mode": mode})
    else:
        df = pd.read_sql("SELECT * FROM trades WHERE status='CLOSED'", conn)
    conn.close()
    return df

def reset_database(mode, start_capital):
    conn = get_connection(mode)
    if DATABASE_URL:
        conn.execute(text("DELETE FROM trades WHERE mode=:mode"), {"mode": mode})
        conn.execute(text("UPDATE portfolio SET capital = :cap WHERE mode = :mode"), {"cap": start_capital, "mode": mode})
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trades")
        cursor.execute("UPDATE portfolio SET capital = ? WHERE id = 1", (start_capital,))
        conn.commit()
    conn.close()
