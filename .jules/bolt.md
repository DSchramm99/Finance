## 2025-05-14 - Parallelization vs API Rate Limiting
**Learning:** While ThreadPoolExecutor speeds up network-bound tasks, high concurrency (e.g., 10+ workers) with yfinance can trigger errors or "possibly delisted" warnings due to rate limiting or connection overhead in some environments.
**Action:** Use moderate worker counts (5-10) and ensure per-thread context is handled correctly for Streamlit's caching.
