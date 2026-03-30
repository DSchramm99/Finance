## 2025-05-15 - [Parallelize Ticker Analysis]
**Learning:** Sequential network-bound tasks in Streamlit (like yfinance downloads) are a major bottleneck. Moving them to background threads using ThreadPoolExecutor significantly improves responsiveness.
**Action:** Use ThreadPoolExecutor with `add_script_run_ctx` to allow concurrent I/O-bound operations while maintaining Streamlit's caching and UI state capabilities.

## 2025-05-15 - [Top-Level Function Caching]
**Learning:** Defining cached functions (@st.cache_data) inside loops or conditional blocks in Streamlit leads to redundant definitions and potential cache misses or overhead.
**Action:** Always move data-fetching or expensive utility functions to the top-level scope of the Streamlit script.
