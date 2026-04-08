## 2025-04-08 - Parallelization and Metadata Optimization
**Learning:** Parallelizing network-bound I/O (like Yahoo Finance price fetching) with `ThreadPoolExecutor` (max_workers=5) provides a significant speedup (~3.5x). Additionally, replacing heavy `yf.Ticker(ticker).info` calls with a targeted Search API request and `@st.cache_data` is a critical bottleneck fix for Streamlit apps.
**Action:** Always prefer `ThreadPoolExecutor` for batch network requests and avoid `yf.Ticker.info` for simple metadata like company names.
