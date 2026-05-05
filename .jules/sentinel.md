## 2025-05-15 - Sensitive Data Exposure in Git
**Vulnerability:** SQLite databases (`live.db`, `trading_live.db`, `trading_test.db`) and `streamlit.log` were being tracked by Git.
**Learning:** Hardcoded tracking of operational state files can lead to unintentional leakage of trade history and system logs if the repository is shared or made public.
**Prevention:** Explicitly exclude `*.db` and `*.log` in `.gitignore` at the project's inception.
