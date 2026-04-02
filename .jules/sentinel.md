## 2025-04-02 - Unified Network Security and Info Leakage Fix
**Vulnerability:** Application hangs (DoS risk) due to missing timeouts on `yfinance` and `requests` calls; Information leakage through raw exception messages in the UI.
**Learning:** `yf.Ticker(ticker).info` is a common source of performance bottlenecks and instability in trading apps; raw `Exception` messages in Streamlit `st.error` can expose internal logic to users.
**Prevention:** Enforce a global 10s timeout on all network-bound calls; centralize metadata retrieval in a framework-agnostic utility with caching and sanitized inputs; use localized, generic error messages for end-users.
