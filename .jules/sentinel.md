## 2025-04-04 - [DoS Prevention and Info Leakage Protection]
**Vulnerability:** Application hangs (DoS) due to missing network timeouts and potential information leakage via raw exception stack traces.
**Learning:** External libraries like `yfinance` and `requests` do not always enforce strict timeouts by default, leading to resource exhaustion. Streamlit applications can expose internal logic if `st.error(e)` is used with raw exception objects.
**Prevention:** Always include a mandatory `timeout=10` in all network requests (`requests.get`, `yf.download`). Sanitize user-facing error messages to be generic and localized. Use `urllib.parse.quote` for any user-controlled input in URLs.
