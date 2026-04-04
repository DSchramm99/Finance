# Bolt's Journal ⚡

## 2026-04-04 - Parallelizing Ticker Analysis
**Learning:** Signal generation for indices like the S&P 500 is slow when done sequentially. Parallelization using `ThreadPoolExecutor` can significantly speed this up. Streamlit's `@st.cache_data` requires a script context to function in background threads.
**Action:** Use `ThreadPoolExecutor` with `add_script_run_ctx` to maintain Streamlit context in worker threads.
