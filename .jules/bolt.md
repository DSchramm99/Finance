## 2026-04-02 - Parallel Ticker Analysis and Optimized Metadata

**Learning:** Parallelizing I/O-bound tasks like `yfinance` data fetching with `ThreadPoolExecutor` provides a massive performance boost (~3.7x - 5.5x speedup). However, in Streamlit, background threads must be explicitly attached to the current script context using `add_script_run_ctx(threading.current_thread())` to avoid "missing ScriptRunContext" warnings and ensure caching works. Additionally, `yf.Ticker(ticker).info` is extremely slow and can be replaced with the Yahoo Search API for lightweight metadata lookup.

**Action:** Always use `ThreadPoolExecutor` for batch network requests in Streamlit and ensure proper context attachment. Prefer targeted APIs over general-purpose info objects for metadata.
