## 2025-05-15 - Enforcing Network Timeouts and Error Sanitization
**Vulnerability:** Application-wide Denial of Service (DoS) risk due to missing timeouts in `yfinance` and `requests` calls, and Information Leakage via raw exception display in Streamlit.
**Learning:** External API dependencies (Yahoo Finance, Wikipedia) can hang indefinitely or leak internal system details (like stack traces) when they fail, compromising both availability and confidentiality.
**Prevention:** Always enforce a mandatory 10s timeout on all network-bound requests and replace raw exception objects with generic, user-friendly error messages in the UI.
