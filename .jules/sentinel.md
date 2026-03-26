# Sentinel Journal 🛡️

Critical security learnings and patterns discovered during development.

## 2025-03-25 - [Atomic Capital Updates]
**Vulnerability:** Race condition in capital updates.
**Learning:** Performing a `SELECT` followed by an `UPDATE` in Python for financial transactions can lead to lost updates if multiple processes or users trigger trade closures simultaneously.
**Prevention:** Always use atomic SQL statements like `UPDATE table SET column = column + ?` for incremental changes to sensitive data.

## 2025-03-25 - [Network Timeout and DoS Protection]
**Vulnerability:** Application hangs due to missing network timeouts.
**Learning:** External API calls (e.g., to Wikipedia or Yahoo Finance) without explicit timeouts can block the application's execution indefinitely if the remote server is unresponsive, leading to a local Denial of Service.
**Prevention:** Always specify a `timeout` parameter for all network requests to ensure the application remains responsive.
