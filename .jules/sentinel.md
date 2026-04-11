## 2026-04-11 - Enforced Timeouts on Network Requests
**Vulnerability:** Application hangs and potential Denial of Service (DoS) due to missing timeout configurations on external API calls (`yfinance` and `requests`).
**Learning:** External network-bound operations must always specify a timeout (e.g., `timeout=10`) to prevent resource exhaustion (worker threads/memory) when services are slow or unresponsive. `yfinance.download` and `requests.get` by default may wait indefinitely or for long OS-level timeouts.
**Prevention:** Enforce a mandatory `timeout` parameter for all network requests. Use the Yahoo Finance Search API for metadata retrieval as a more efficient and securable alternative to `yf.Ticker.info`.
