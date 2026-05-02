## 2026-03-25 - Sensitive Files Tracked in Git
**Vulnerability:** Binary database files (`live.db`, `trading_live.db`, `trading_test.db`) and application logs (`streamlit.log`) were tracked in the Git repository.
**Learning:** Incomplete `.gitignore` and manual additions allowed sensitive operational data and stateful database files to be exposed in the codebase.
**Prevention:** Ensure all stateful files, logs, and sensitive environment-specific artifacts are explicitly excluded in `.gitignore` from the project's inception. Regularly audit `git ls-files` to ensure no sensitive files have slipped into the index.
