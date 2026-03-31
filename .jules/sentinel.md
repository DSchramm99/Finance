## 2025-05-15 - Global Network Timeout Enforcement
**Vulnerability:** Potential Denial of Service (DoS) and application hangs due to missing timeouts on external network requests (Yahoo Finance and Wikipedia).
**Learning:** Multiple entry points for market data (yfinance and requests) lacked explicit timeout configurations, which could lead to resource exhaustion if external APIs respond slowly or hang.
**Prevention:** Enforce a mandatory `timeout=10` parameter for all `requests.get()` and `yf.download()` calls across the codebase to ensure the application fails securely and remains responsive.
