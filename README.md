# 📊 Professional Trading System

## Overview

This project is a **quantitative stock screening tool** built with **Python and Streamlit**.
It scans major stock indices (e.g. S&P 500, Nasdaq 100, DAX) and identifies the **top 5 trading opportunities**.

---

## 🚀 How to Access the App

You have two ways to run and access this app: **locally on your network** or **permanently in the cloud**.

### 1. Local Network Access (e.g., from your Phone)
If you run the app on your Mac/PC, you can access it from your phone as long as both are on the **same Wi-Fi**.

1.  **Start the app on your computer:**
    ```bash
    streamlit run app.py
    ```
2.  **Find your Local IP:** Streamlit will show you two URLs in the terminal:
    - `Local URL: http://localhost:8501` (for your computer)
    - `Network URL: http://192.168.x.x:8501` (**use this on your phone!**)
3.  **Keep it running:** For this to work, your computer **must stay on and the app must keep running**. If you close your Mac, the app stops.

### 2. Permanent Cloud Deployment (Recommended)
To access the app from **anywhere in the world** at **any time** (without leaving your computer on), you should deploy it to a cloud provider.

#### Streamlit Community Cloud (Free & Easiest)
1. Push this code to a **GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub.
3. Select this repository and click **Deploy**.
4. You will get a permanent link (e.g., `https://your-app.streamlit.app`) that works on any device.

---

## 💾 Saving your Trades (Persistence)

By default, the app saves trades in a local file (`trading_live.db`).
- **If you use local access:** The trades are saved on your computer.
- **If you use the cloud:** You should connect a **centralized database** so your trades aren't lost when the cloud server restarts.

### Connecting a Centralized Database
Set the `DATABASE_URL` environment variable in your cloud provider settings (e.g., a PostgreSQL URL from Supabase or Neon):
```bash
export DATABASE_URL="postgresql://user:password@host:port/dbname"
```
The app will automatically detect this and use the remote database for both your computer and your phone.

---

## 🛠 Setup & Technical Details

### Local Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Docker Support
```bash
docker build -t trading-system .
docker run -p 8501:8501 trading-system
```

---

## 📈 Tech Stack
- **Frontend:** Streamlit
- **Data:** yfinance, Pandas
- **Database:** SQLite (local) or any SQL DB via `DATABASE_URL`.
