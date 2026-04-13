## 2024-04-13 - [Streamlit Threading Context]
**Learning:** Functions decorated with `@st.cache_data` cannot be called from background threads unless the Streamlit script run context is manually attached to the thread.
**Action:** Always import `get_script_run_ctx` and `add_script_run_ctx` from `streamlit.runtime.scriptrunner` and apply them to worker threads in a `ThreadPoolExecutor`.
