## 2025-04-06 - Network Timeout and Error Sanitization
**Vulnerability:** Denial of Service (DoS) and Information Leakage.
**Learning:** External network calls (requests, yfinance) lacked timeouts, potentially hanging the application. Error messages in the monitoring loop exposed raw exception details.
**Prevention:** Always enforce a 10s timeout on network-bound operations. Sanitize user-facing error messages to avoid leaking stack traces or internal logic, and localize them for consistent UX.
