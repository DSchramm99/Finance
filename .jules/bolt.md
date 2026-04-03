## 2026-04-03 - Parallelized Ticker Analysis
**Learning:** Parallelizing I/O-bound tasks like yfinance downloads with `ThreadPoolExecutor` significantly improves UX in Streamlit, but requiring `add_script_run_ctx` from `streamlit.runtime.scriptrunner` is essential for thread safety with Streamlit's caching.
**Action:** Use `ThreadPoolExecutor` with a conservative `max_workers` (e.g., 5) and `add_script_run_ctx` for all multi-ticker processing in the future.
