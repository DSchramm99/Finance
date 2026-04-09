## 2025-04-09 - Global Network Timeouts for DoS Prevention
**Vulnerability:** Application hangs and potential Denial of Service (DoS) due to missing timeouts on external network requests (`requests.get` and `yfinance.download`).
**Learning:** External APIs (Yahoo Finance, Wikipedia) can be slow or unresponsive, causing the Streamlit UI to freeze or the scanner to hang indefinitely if no timeout is specified.
**Prevention:** Always enforce a mandatory timeout (e.g., `timeout=10`) on all network-bound calls using `requests` or third-party wrappers like `yfinance`.
