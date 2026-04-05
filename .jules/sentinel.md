## 2025-04-05 - Network Security Enhancement and Info Leakage Fix
**Vulnerability:** Application hangs due to missing timeouts in network calls (DoS) and potential info leakage in error messages.
**Learning:** External APIs (Yahoo Finance, Wikipedia) can be slow or unresponsive, leading to resource exhaustion. Verbose error messages in Streamlit can leak stack traces or internal logic to users.
**Prevention:** Always implement a mandatory timeout (e.g., 10s) for all external network requests. Use sanitized, generic error messages in user-facing components to prevent information disclosure.
