## 2025-05-15 - [Yahoo Finance Metadata Bottleneck]
**Learning:** Using `yf.Ticker(ticker).info` is significantly slower than using a direct call to the Yahoo Finance Search API for basic metadata like company names. The `info` property fetches a large, complex dictionary, while the search API is lightweight and targeted.
**Action:** Always prefer the Yahoo Finance Search API for simple metadata retrieval (name, sector, industry) when using `yfinance`. Combine with `@st.cache_data` in Streamlit for near-instant repeat lookups.

## 2025-05-15 - [ThreadPoolExecutor vs. Result Ordering]
**Learning:** `as_completed` in `ThreadPoolExecutor` returns futures as they finish, which can shuffle the order of results. In a UI where the input order matters (e.g., scanning a known index), this can be confusing to the user.
**Action:** When order matters, use a mapping (e.g., `results_map[ticker] = result`) and reconstruct the results list from the original input list after the parallel block finishes.
