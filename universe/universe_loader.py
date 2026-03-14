import pandas as pd
import requests
from io import StringIO


# =====================================================
# Safe Wikipedia Loader
# =====================================================

def load_wikipedia_table(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tables = pd.read_html(response.text)

    return tables


# =====================================================
# Helper: Extract Ticker Column Automatically
# =====================================================

def extract_tickers_from_tables(tables):

    for df in tables:

        for col in df.columns:

            if isinstance(col, str):

                if any(keyword in col.lower() for keyword in ["ticker", "symbol"]):

                    return df[col].dropna().astype(str).tolist()

    raise ValueError("No ticker/symbol column found.")


# =====================================================
# Local CSV Loader (NEW)
# =====================================================

import os

def load_local_csv(filename):

    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "indices", filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} not found in universe/indices/")

    return pd.read_csv(file_path)


# =====================================================
# Dow Jones (NEW - Local CSV)
# =====================================================

def load_dowjones():

    df = load_local_csv("dowjones.csv")

    # Ticker ist zweite Spalte
    ticker_column = df.columns[1]

    return (
        df[ticker_column]
        .dropna()
        .astype(str)
        .tolist()
    )


# =====================================================
# TecDAX (NEW - Local CSV)
# =====================================================

def load_tecdax():

    df = load_local_csv("tecdax.csv")

    # Ticker ist zweite Spalte
    ticker_column = df.columns[1]

    return (
        df[ticker_column]
        .dropna()
        .astype(str)
        .tolist()
    )


# =====================================================
# Index Loaders (UNCHANGED)
# =====================================================

def load_sp500():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = load_wikipedia_table(url)

    return tables[0]["Symbol"].dropna().astype(str).tolist()


def load_nasdaq100():

    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    tables = load_wikipedia_table(url)

    return extract_tickers_from_tables(tables)


def load_dax():

    url = "https://en.wikipedia.org/wiki/DAX"
    tables = load_wikipedia_table(url)

    return extract_tickers_from_tables(tables)


# =====================================================
# Optional: Combined Universe
# =====================================================

def load_universe():

    universe = []

    try:
        universe += load_sp500()
    except Exception:
        pass

    try:
        universe += load_nasdaq100()
    except Exception:
        pass

    try:
        universe += load_dax()
    except Exception:
        pass

    try:
        universe += load_dowjones()
    except Exception:
        pass

    try:
        universe += load_tecdax()
    except Exception:
        pass

    return list(set([t for t in universe if isinstance(t, str)]))


# =====================================================
# Index Selector
# =====================================================

def get_index_universe(index_name):

    if index_name == "S&P 500":
        return load_sp500()

    elif index_name == "Nasdaq 100":
        return load_nasdaq100()

    elif index_name == "Dow Jones":
        return load_dowjones()

    elif index_name == "DAX":
        return load_dax()

    elif index_name == "TecDAX":
        return load_tecdax()

    elif index_name == "All":
        return load_universe()

    else:
        raise ValueError(f"Unknown index: {index_name}")