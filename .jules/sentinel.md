## 2025-05-04 - Exposure of sensitive operational files
**Vulnerability:** SQLite database files (`live.db`, `trading_live.db`, `trading_test.db`) and execution logs (`streamlit.log`) were being tracked by Git.
**Learning:** Operational data files and logs were not included in `.gitignore`, leading to the exposure of sensitive trade data and portfolio information in the repository history.
**Prevention:** Always include `*.db` and `*.log` in the root `.gitignore` at the start of a project and verify that no sensitive data files are added to the Git index.
