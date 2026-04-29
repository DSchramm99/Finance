## 2025-04-29 - Streamlit Caching Anti-pattern
**Learning:** Defining `@st.cache_data` functions inside a loop or a function body causes Streamlit to re-register the cache constantly, leading to zero cache hits and degraded performance. Additionally, propagating context to worker threads is required for caching to work in parallel.
**Action:** Always define cached helper functions at the module level. Use `streamlit.runtime.scriptrunner` to propagate context to `ThreadPoolExecutor` workers.
