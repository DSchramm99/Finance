## 2025-05-15 - [Parallel Ticker Analysis]
**Learning:** Sequential I/O for multiple ticker analysis (100-500 tickers) was the primary bottleneck. Parallelizing with `ThreadPoolExecutor` and `as_completed` yielded a ~6x speedup (0.31s -> 0.05s per ticker). Metadata fetching (company names) was also parallelized for the final top 5 results.
**Action:** Always consider parallelizing network-bound operations like `yfinance` downloads, especially when processing list-based data in Streamlit.
