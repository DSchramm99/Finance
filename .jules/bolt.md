## 2025-05-14 - ThreadPoolExecutor Context Propagation
**Learning:** In Streamlit, background threads must have the script execution context applied *inside* the worker function to reliably access cached resources like @st.cache_data. Applying it to executor._threads after submission is prone to race conditions where the task might start before the context is set.
**Action:** Wrap worker functions in a helper that calls add_script_run_ctx(threading.current_thread(), ctx) as the first step of execution.
