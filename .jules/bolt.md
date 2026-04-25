# Bolt's Journal - Critical Learnings Only

## 2025-05-15 - Parallelizing Ticker Analysis in Streamlit
**Learning:** Sequential processing of stock tickers with `yfinance` is a major bottleneck due to network latency per request. Using `ThreadPoolExecutor` can significantly speed up the analysis of a stock universe. However, when using multi-threading within a Streamlit app, we must ensure that the Streamlit script context is properly propagated to the worker threads using `add_script_run_ctx` if they call cached functions or use Streamlit primitives.
**Action:** Always use `streamlit.runtime.scriptrunner.add_script_run_ctx` when initializing worker threads in Streamlit to maintain context and ensure `@st.cache_data` works as expected.
