# 📊 Professional Trading System

## Overview

This project is a **quantitative stock screening tool** built with **Python and Streamlit**.
It scans major stock indices (e.g. S&P 500, Nasdaq 100, DAX) and identifies the **top 5 trading opportunities** based on a rule-based scoring model.

The application allows you to track trades in both **TEST** and **LIVE** portfolios, supporting both standard and leveraged trading modes.

---

## 🚀 Getting Started

### Local Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App:**
   ```bash
   streamlit run app.py
   ```
   By default, the app uses local SQLite databases (`trading_test.db` and `trading_live.db`).

### Portability and Cloud Deployment

The app is designed to be portable and can be deployed anywhere (e.g., Streamlit Community Cloud, Heroku, AWS).

#### Docker

You can run the app using Docker:
```bash
docker build -t trading-system .
docker run -p 8501:8501 trading-system
```

#### Centralized Database

To share your portfolio across different devices or instances, you can use a centralized database (like PostgreSQL). Set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://user:password@host:port/dbname"
streamlit run app.py
```

If `DATABASE_URL` is set, the app will automatically use the specified database instead of local SQLite files.

---

## 📈 Data Source

Market data is retrieved from **Yahoo Finance** via the `yfinance` package. The system evaluates each stock using trend analysis, volatility assessment, and risk-reward calculation.

---

## 🧠 Scoring System

Each stock receives:
- **Trend Score:** Measures momentum relative to SMA20.
- **Risk Score:** Measures relative volatility using ATR.
- **Final Score:** A weighted combination (60% Trend, 40% Risk).

---

## 💰 Trade Management

- **Signals:** Get automated buy recommendations for major indices.
- **Portfolio:** Track open and closed trades.
- **Monitoring:** Real-time trailing stop calculation (Chandelier Exit) to help manage open positions.

---

## 🛠 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Data:** [yfinance](https://github.com/ranaroussi/yfinance), [Pandas](https://pandas.pydata.org/)
- **Visuals:** [Plotly](https://plotly.com/)
- **Database:** SQLite (default) or any SQLAlchemy-supported DB via `DATABASE_URL`.
