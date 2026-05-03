## 2026-05-03 - [Information Leakage] Sensitive Files in Git
**Vulnerability:** SQLite databases (`.db`) and log files (`.log`) were being tracked by Git.
**Learning:** These files can contain sensitive operational data, trade history, and system information that should not be shared or versioned.
**Prevention:** Always include `*.db` and `*.log` in `.gitignore` and use `git rm --cached` to stop tracking them if they were already added.
