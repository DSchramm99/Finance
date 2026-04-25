## 2026-04-25 - Sensitive File Exposure
**Vulnerability:** Binary database files (`.db`) and execution logs (`.log`) were tracked in version control.
**Learning:** `streamlit.log` leaked internal application state and external connection details, while `.db` files could expose sensitive user portfolio data.
**Prevention:** Add `*.db` and `*.log` to `.gitignore` and use `git rm --cached` to prune them from the repository history if they were previously committed.
