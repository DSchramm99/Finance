## 2025-05-15 - Parallel Ticker Analysis in Streamlit

**Learning:** Benchmarking 20 tickers in `app.py` shows a significant performance gain: bulk downloading ticker data with `yf.download` is ~3x faster than sequential execution (reducing time from ~4.8s to ~1.6s). However, `ThreadPoolExecutor` is preferred over bulk download in this specific UI context to maintain granular progress bar updates for the user.
**Action:** Use `ThreadPoolExecutor(max_workers=5)` for multi-ticker analysis in Streamlit to balance speed and user feedback (UX).
