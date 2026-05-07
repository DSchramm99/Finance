# Deployment Guide

This guide explains how to make your trading system available everywhere and ensure your data is safe.

## 1. Hosting Options

### Option A: Streamlit Community Cloud (Free)
*Best for: Quick, free access from any browser.*

1. **GitHub:** Create a private or public GitHub repository and push your code.
2. **Deploy:** Log in to [Streamlit Cloud](https://share.streamlit.io/) and point it to your repo.
3. **Secrets:** If you use a remote database, add your `DATABASE_URL` in the "Secrets" section of the Streamlit dashboard:
   ```toml
   DATABASE_URL = "postgresql://..."
   ```

### Option B: Self-Hosting (Docker)
*Best for: Using your own server or NAS.*

1. **Build:** `docker build -t trading-app .`
2. **Run:** `docker run -d -p 8501:8501 --env DATABASE_URL=... trading-app`

---

## 2. Database (The "Brain")

If you want to use the app on both your phone and your computer and see the **same trades**, you need a central database.

### Recommended: Supabase (Free Tier)
1. Create a project on [Supabase.com](https://supabase.com).
2. Go to Project Settings -> Database.
3. Copy the **Connection String** (URI).
4. Set this as your `DATABASE_URL` environment variable.

The app will automatically create the tables (`portfolio` and `trades`) the first time it connects.

---

## 3. Accessing from Phone

### On your home Wi-Fi:
1. Run the app on your computer.
2. Open your phone's browser.
3. Type the **Network URL** shown in your computer's terminal (e.g., `http://192.168.1.50:8501`).

### From anywhere (LTE/Coffee Shop):
1. Use **Option A** (Streamlit Cloud) or **Option B** (Docker on a public server).
2. Use the provided `https://...` link.
