## 2026-04-03 - Network Resilience and Error Sanitization
**Vulnerability:** Potential Denial of Service (DoS) via application hangs and Information Leakage through verbose error messages.
**Learning:** External network calls (via `requests` or `yfinance`) without explicit timeouts can cause the Streamlit application to hang indefinitely if the provider is slow. Additionally, displaying raw exception objects in the UI can leak internal logic or stack traces.
**Prevention:** Always enforce a mandatory 10-second timeout on all network requests and use localized, generic error messages for user-facing feedback instead of raw exceptions.
