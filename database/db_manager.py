import sqlite3
import os
import pandas as pd
from datetime import datetime

# =====================================================
# Database Selector
# =====================================================

DB_PATHS = {
    "TEST": "trading_test.db",
    "LIVE": "trading_live.db"
}

def get_connection(mode):
    if mode == "TEST":
        db_path = "trading_test.db"
    else:
        db_path = "trading_live.db"

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# Initialize Database
# =====================================================

def init_db(mode, start_capital=2000):
    conn = get_connection(mode)
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
    cursor = conn.cursor()
    cursor.execute("SELECT capital FROM portfolio WHERE id=1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def set_capital(amount, mode="TEST"):
    conn = get_connection(mode)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM portfolio")
    cursor.execute(
        "INSERT INTO portfolio (id, capital) VALUES (1, ?)",
        (amount,)
    )
    conn.commit()
    conn.close()


# =====================================================
# Trade Functions
# =====================================================

def add_trade(mode, ticker, entry, stop, tp, position_value, fees, leverage=1.0):
    conn = get_connection(mode)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO trades
        (ticker, entry, stop, take_profit, position_value, fees, status, timestamp, leverage)
        VALUES (?, ?, ?, ?, ?, ?, 'OPEN', ?, ?)
    """, (ticker, entry, stop, tp, position_value, fees, timestamp, leverage))

    conn.commit()
    conn.close()

def close_trade(mode, trade_id, exit_price, sell_fee = 0):
    conn = get_connection(mode)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
    trade = cursor.fetchone()

    if not trade:
        conn.close()
        return

    entry = trade["entry"]
    position_value = trade["position_value"]
    fees = trade["fees"]
    # Ensure leverage is at least 1.0 if None
    leverage = trade["leverage"] if trade["leverage"] is not None else 1.0

    quantity = position_value / entry

    # Leveraged profit calculation
    gross_profit = (exit_price - entry) * quantity * leverage
    profit = gross_profit - sell_fee - fees

    cursor.execute("""
        UPDATE trades
        SET exit_price = ?,
            profit = ?,
            status = 'CLOSED'
        WHERE id = ?
    """, (exit_price, profit, trade_id))

    # Atomic update to prevent race conditions
    cursor.execute("UPDATE portfolio SET capital = capital + ? WHERE id=1", (profit,))

    conn.commit()
    conn.close()

def get_open_trades(mode):
    conn = get_connection(mode)
    df = pd.read_sql_query(
        "SELECT * FROM trades WHERE status='OPEN'",
        conn
    )
    conn.close()
    return df

def delete_trade(mode, trade_id):
    conn = get_connection(mode)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades WHERE id=?", (trade_id,))
    conn.commit()
    conn.close()


def update_trade_exit(mode, trade_id, exit_price):
    conn = get_connection(mode)
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
    df = pd.read_sql("SELECT * FROM trades WHERE status='CLOSED'", conn)
    conn.close()
    return df

def reset_database(mode, start_capital):
    conn = get_connection(mode)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades")
    cursor.execute("UPDATE portfolio SET capital = ? WHERE id = 1", (start_capital,))
    conn.commit()
    conn.close()
