## 2026-04-24 - Optimized Company Name and Parallel Scanning
**Learning:** Parallelizing ticker analysis in Streamlit with ThreadPoolExecutor requires explicit script context propagation using a wrapper that calls `sr.add_script_run_ctx(ctx)` inside the worker thread to enable safe caching.
**Action:** Always use a context wrapper for background tasks in Streamlit that interact with cached functions.
