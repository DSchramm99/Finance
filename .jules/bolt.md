## 2026-04-06 - Streamlit Threading Context
**Learning:** Background threads in Streamlit must explicitly capture and apply the script execution context (`get_script_run_ctx()` and `add_script_run_ctx()`) to safely use Streamlit features like `@st.cache_data`.
**Action:** Always pass the parent thread's context to `ThreadPoolExecutor` workers and call `add_script_run_ctx` inside the worker function.

## 2026-04-06 - Yahoo Finance Search API
**Learning:** `yf.Ticker(ticker).info` is extremely slow as it fetches a massive JSON for each ticker. The Yahoo Finance search API (`/v1/finance/search`) is much faster for simple metadata like company names.
**Action:** Use the search API for lightweight metadata lookups instead of the full `Ticker.info`.
