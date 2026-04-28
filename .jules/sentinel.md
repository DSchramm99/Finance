## 2025-05-15 - Repository Hardening: Ignoring Sensitive Files and Network Robustness
**Vulnerability:** Sensitive files like `*.db` and `*.log` were being tracked by Git, potentially exposing trade history and system details. Also, lack of timeouts on external network requests (`requests.get`) posed a DoS risk.
**Learning:** SQLite databases and server logs are often generated during runtime and should never be part of the Git history to prevent data leakage. Network requests without timeouts can cause the application to hang indefinitely.
**Prevention:** Always include `*.db` and `*.log` in `.gitignore` from the start and explicitly remove them from the index if they were already added. Use the `timeout` parameter in all `requests` calls to enforce network robustness.
