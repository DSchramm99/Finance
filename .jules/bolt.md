## 2025-05-15 - Parallel Ticker Analysis in Streamlit
**Learning:** Parallelizing network-bound tasks in Streamlit requires careful handling of the script context using `get_script_run_ctx` and `add_script_run_ctx` to ensure that `@st.cache_data` and other Streamlit features function correctly in worker threads.
**Action:** Always capture the main thread's context and apply it to worker threads when using Streamlit's reactive or cached components in a `ThreadPoolExecutor`.

## 2025-05-15 - Deterministic Order in Parallel Monitoring
**Learning:** Using `as_completed` in a monitoring loop can cause row flickering or non-deterministic ordering in the UI, which is bad for UX.
**Action:** Iterate over the original list of futures instead of using `as_completed` when the order of results matters for the display.
