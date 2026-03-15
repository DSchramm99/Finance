import sqlite3
import os
import pandas as pd

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

    # ⭐ WICHTIG:
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
            status TEXT
        )
    """)

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

def add_trade(mode, ticker, entry, stop, tp, position_value, fees):

    conn = get_connection(mode)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades
        (ticker, entry, stop, take_profit, position_value, fees, status)
        VALUES (?, ?, ?, ?, ?, ?, 'OPEN')
    """, (ticker, entry, stop, tp, position_value, fees))

    conn.commit()
    conn.close()

def close_trade(mode, trade_id, exit_price, sell_fee = 0):

    conn = get_connection(mode)
    cursor = conn.cursor()

    # Trade holen
    cursor.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
    trade = cursor.fetchone()

    if not trade:
        return

    entry = trade["entry"]
    position_value = trade["position_value"]
    fees = trade["fees"]

    # Gewinn berechnen
    quantity = position_value / entry
    quantity = position_value / entry

    gross_profit = (exit_price - entry) * quantity

    profit = gross_profit - sell_fee - fees

    # Trade schließen
    cursor.execute("""
        UPDATE trades
        SET exit_price = ?,
            profit = ?,
            status = 'CLOSED'
        WHERE id = ?
    """, (exit_price, profit, trade_id))

    # Kapital aktualisieren
    cursor.execute("SELECT capital FROM portfolio WHERE id=1")
    capital = cursor.fetchone()["capital"]

    new_capital = capital + profit

    cursor.execute("UPDATE portfolio SET capital = ? WHERE id=1", (new_capital,))

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

    # Trades löschen
    cursor.execute("DELETE FROM trades")

    # Kapital neu setzen
    cursor.execute("UPDATE portfolio SET capital = ? WHERE id = 1", (start_capital,))

    conn.commit()
    conn.close()
