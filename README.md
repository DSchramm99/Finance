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

# 📈 Data Source

Market data is retrieved from:

* **Yahoo Finance**
* via the Python package `yfinance`

Each ticker loads **2 years of daily price data** including:

* Open
* High
* Low
* Close
* Adjusted prices

The data is cached using **Streamlit caching** to improve performance.

---

# 📊 Technical Indicators

The following indicators are calculated for every stock:

### Simple Moving Averages

| Indicator | Description                   |
| --------- | ----------------------------- |
| SMA20     | 20-day simple moving average  |
| SMA50     | 50-day simple moving average  |
| SMA200    | 200-day simple moving average |

These indicators are used to evaluate **short, medium and long-term trend direction**.

---

### Average True Range (ATR)

ATR is used as a **volatility proxy**.

Simplified calculation used in this project:

ATR = Rolling Mean of:

High − Low

Window:

14 days

ATR is later used to determine **stop loss distance**.

---

# 🧠 Scoring System

Each stock receives three scores:

1. **Trend Score**
2. **Risk Score**
3. **Final Score**

---

# 📈 Trend Score

The trend score measures how strongly the current price is positioned relative to the **20-day moving average**.

Formula:

TrendRaw = (Close − SMA20) / SMA20

TrendScore = clamp(50 + TrendRaw × 200, 0, 100)

Interpretation:

| Trend Score | Meaning          |
| ----------- | ---------------- |
| 0–30        | Strong downtrend |
| 30–50       | Weak trend       |
| 50          | Neutral          |
| 50–70       | Moderate uptrend |
| 70–100      | Strong uptrend   |

The scaling factor `200` amplifies small differences between price and SMA20.

---

# ⚠️ Risk Score

The risk score measures **relative volatility** using ATR.

Formula:

Volatility = ATR / Close

RiskScoreRaw = 100 − (Volatility × 500)

RiskScore = clamp(RiskScoreRaw, 0, 100)

Interpretation:

| Risk Score | Meaning                 |
| ---------- | ----------------------- |
| 0–30       | Very volatile           |
| 30–60      | Moderate volatility     |
| 60–100     | Stable / low volatility |

For user presentation, the system displays:

Risk Display = 100 − RiskScore

This makes **lower values represent lower risk**, which is often more intuitive.

---

# ⭐ Final Score

The final score combines trend and risk.

Formula:

FinalScore = 0.6 × TrendScore + 0.4 × RiskScore

Weighting rationale:

* Trend is slightly more important (60%)
* Risk still significantly influences ranking (40%)

Stocks are ranked by **highest Final Score**.

The system displays the **Top 5 opportunities**.

---

# 💰 Trade Level Calculation

For each selected stock the system calculates:

* Entry Price
* Stop Loss
* Take Profit

---

## Entry Price

Entry depends on trend strength.

If:

TrendScore > 65

Entry = Current Close

Otherwise:

Entry = SMA20

Rationale:

* Strong trends allow **momentum entry**
* Weaker trends prefer **pullback entry near the moving average**

---

##
