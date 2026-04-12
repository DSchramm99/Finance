## 2026-04-12 - [Enforce timeouts on all network requests]
**Vulnerability:** Indefinite application hangs during network requests (DoS risk).
**Learning:** Default behavior for many Python libraries (like `requests`) is to wait indefinitely, which can be exploited to cause Denial of Service.
**Prevention:** Always specify a `timeout` parameter for all network-bound calls.
