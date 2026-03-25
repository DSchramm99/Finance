## 2025-03-14 - Parallelize Ticker Analysis
**Learning:** Sequential processing of multiple stock tickers using `yfinance` in `app.py` is a major bottleneck due to network latency. The original implementation takes several minutes for large indices.
**Action:** Use `ThreadPoolExecutor` and `as_completed` to parallelize I/O-bound operations like ticker analysis and metadata fetching.
