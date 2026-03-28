# Sentinel Security Journal

## 2025-03-28 - Missing Network Timeouts
**Vulnerability:** Indefinite application hangs during network requests.
**Learning:** External calls to Wikipedia (via `requests`) and Yahoo Finance (via `yfinance`) lacked timeout parameters. This could lead to Denial of Service (DoS) where application threads are exhausted waiting for unresponsive remote servers.
**Prevention:** All network requests MUST include a `timeout=10` parameter (or equivalent) to ensure the application fails gracefully and remains responsive.

## Reusable Security Patterns
- **Mandatory Timeouts:** Always use `timeout=10` for `requests.get`, `requests.post`, and `yf.download`.
- **Input Sanitization:** (Placeholder for future findings)
- **Parameterized Queries:** (Placeholder for future findings)
