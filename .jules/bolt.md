## 2024-04-18 - Parallelizing Ticker Analysis and Monitoring
**Learning:** Parallelizing ticker analysis with `ThreadPoolExecutor` significantly reduces UI wait times for index scans and portfolio loading (up to 9x speedup). Streamlit context must be explicitly passed to worker threads using `add_script_run_ctx` to maintain functionality like caching.
**Action:** Always use `ThreadPoolExecutor` for batch network/I/O operations in Streamlit apps and wrap worker functions with `add_script_run_ctx`.
