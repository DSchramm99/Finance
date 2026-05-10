# 📊 Professional Trading System

## Overview

This project is a **quantitative stock screening tool** built with **Python and Streamlit**.
It scans major stock indices (e.g. S&P 500, Nasdaq 100, DAX) and identifies the **top 5 trading opportunities** based on a rule-based scoring model.

The system evaluates each stock using a combination of:
* Trend analysis
* Volatility / risk assessment
* Risk-reward calculation

The result is a ranked list of potential trades including:
* Entry price
* Stop-loss level
* Take-profit target
* Trend score
* Risk score
* Combined final score

The application also provides an interactive **price chart with moving averages and trade levels**.

---

## 📈 Data Source

Market data is retrieved from **Yahoo Finance** via the `yfinance` package.
Each ticker loads **2 years of daily price data** including Open, High, Low, Close, and Adjusted prices.

---

## 📊 Technical Indicators

The following indicators are calculated for every stock:

### Simple Moving Averages
| Indicator | Description |
| --------- | ----------- |
| SMA20     | 20-day simple moving average |
| SMA50     | 50-day simple moving average |
| SMA200    | 200-day simple moving average |

These indicators are used to evaluate **short, medium and long-term trend direction**.

### Average True Range (ATR)
ATR is used as a **volatility proxy**.
`ATR = Rolling Mean of (High - Low)` over a 14-day window.
ATR is used to determine **stop loss distance** and risk scoring.

---

## 🧠 Scoring System

Each stock receives three scores:

### 1. Trend Score
Measures how strongly the current price is positioned relative to the SMA20.
`TrendScore = clamp(50 + ((Close - SMA20) / SMA20) * 200, 0, 100)`

### 2. Risk Score
Measures **relative volatility** using ATR.
`RiskScore = clamp(100 - (ATR / Close * 500), 0, 100)`
*Note: In the UI, higher risk scores indicate higher volatility (inverted for intuition).*

### 3. Final Score
Combines trend and risk.
`FinalScore = 0.6 * TrendScore + 0.4 * RiskScore`

---

## 💰 Trade Management

- **Signals:** Get automated buy recommendations for major indices.
- **Portfolio:** Track open and closed trades with real-time monitoring.
- **Monitoring:** Uses Chandelier Exit for trailing stops to protect profits.

---

## 🚀 Deployment & Portability

The app is designed to be portable and can be deployed anywhere.

### Local Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Cloud Database (Supabase)
The app is configured to use **Supabase** for persistent storage. Ensure you add `SUPABASE_URL` and `SUPABASE_KEY` to your Streamlit secrets or environment variables to sync trades across devices.

---

## 🛠 Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Data:** [yfinance](https://github.com/ranaroussi/yfinance)
- **Database:** Supabase (Remote) or SQLite (Local fallback)
