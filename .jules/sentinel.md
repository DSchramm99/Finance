## 2025-05-14 - Sensitive Files in Version Control
**Vulnerability:** SQLite databases (`.db`) and application logs (`.log`) were being tracked by Git.
**Learning:** Operational data like `trading_live.db` and `streamlit.log` were included in the repository, potentially exposing trade history, capital, and internal system details.
**Prevention:** Always include `*.db` and `*.log` in `.gitignore` from the start of a project to prevent sensitive data leakage.
