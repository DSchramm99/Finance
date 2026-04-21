## 2025-03-25 - Prevention of DoS via Network Timeouts
**Vulnerability:** External API calls (requests.get) and yfinance Ticker info lookups were performed without explicit timeouts, potentially leading to application hangs if the remote server is slow or unresponsive.
**Learning:** Defaulting to no timeout in network-dependent applications creates a Denial of Service (DoS) risk where worker threads can be exhausted by hanging connections.
**Prevention:** Always implement a mandatory timeout (e.g., 10 seconds) for all network requests. Centralize external lookups into "safe" helpers that handle errors and timeouts gracefully.

## 2025-03-25 - Sensitive Data Exposure in Repository
**Vulnerability:** Local database files (*.db) and application logs (*.log) were not explicitly ignored in .gitignore.
**Learning:** Local development artifacts often contain sensitive state (e.g., trading history, capital) or internal system details that should not be committed to version control.
**Prevention:** Maintain a strict .gitignore that excludes all data storage and log files by default.
