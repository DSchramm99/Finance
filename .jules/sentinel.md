# Sentinel's Security Journal

## 2025-03-25 - Sensitive Files Tracked in Git
**Vulnerability:** Sensitive SQLite database files (`live.db`, `trading_live.db`, `trading_test.db`) and application logs (`streamlit.log`) were being tracked by Git.
**Learning:** SQLite databases often contain trade history, capital information, and potentially sensitive operational data. Logs can expose internal IP addresses and application flow.
**Prevention:** Always add `*.db` and `*.log` to `.gitignore` at the start of a project and verify with `git ls-files` that they aren't being tracked.
