# Bolt's Journal - Performance Learnings

## 2026-03-26 - Initial Assessment
**Learning:** Found sequential I/O-bound loops in `app.py` that perform network requests to Yahoo Finance for each ticker in a universe. This is a significant bottleneck for large universes like S&P 500.
**Action:** Use `ThreadPoolExecutor` to parallelize these requests while maintaining UI updates from the main thread.
