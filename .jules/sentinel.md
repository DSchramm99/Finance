## 2026-05-01 - Sensitive Files Tracked in Git
**Vulnerability:** SQLite database files (`live.db`, `trading_live.db`, `trading_test.db`) and log files (`streamlit.log`) were being tracked by Git.
**Learning:** Forgetting to ignore database and log files can lead to sensitive operational data and user information being leaked in the repository history.
**Prevention:** Always include `*.db` and `*.log` in `.gitignore` at the start of a project.

## 2026-05-01 - Missing Network Timeouts
**Vulnerability:** External requests using `requests.get` in `universe/universe_loader.py` lacked a timeout parameter.
**Learning:** Missing timeouts can lead to Denial of Service (DoS) if an external service hangs, causing application threads to be indefinitely blocked.
**Prevention:** Always specify a `timeout` parameter for all network requests.
