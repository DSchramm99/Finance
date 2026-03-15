import sqlite3

DB_NAME = "trading_system.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
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
        position_value REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def get_capital():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT capital FROM portfolio WHERE id=1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    return None


def set_capital(amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM portfolio")
    cursor.execute("INSERT INTO portfolio (id, capital) VALUES (1, ?)", (amount,))

    conn.commit()
    conn.close()


def add_trade(ticker, entry, stop, tp, position_value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades (ticker, entry, stop, take_profit, position_value)
        VALUES (?, ?, ?, ?, ?)
    """, (ticker, entry, stop, tp, position_value))

    conn.commit()
    conn.close()