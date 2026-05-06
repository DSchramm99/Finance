## 2025-05-06 - Sensitive Data Leakage Prevention
**Vulnerability:** SQLite database files (*.db) and application logs (*.log) were tracked in the Git repository. These files can contain sensitive trade data, capital information, and operational details.
**Learning:** Default project templates or initial setups might overlook sensitive local state files in .gitignore. Even if data is not "secret" like an API key, it is still sensitive user data.
**Prevention:** Explicitly ignore all database and log extensions (*.db, *.log) in .gitignore and verify with `git ls-files` that no such files are tracked.

## 2025-05-06 - Network Request Security
**Vulnerability:** Wikipedia scraping via `requests.get` was performed without a timeout, and `pd.read_html` was using a deprecated signature that could lead to reliability issues.
**Learning:** Lack of timeouts in network requests can lead to Denial of Service (DoS) where worker threads are hung indefinitely by a slow or malicious server.
**Prevention:** Always specify a `timeout` in `requests.get` calls and follow library-specific best practices (like using `StringIO` for `pd.read_html` in newer Pandas versions).
