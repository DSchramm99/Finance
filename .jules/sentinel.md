# Sentinel Security Journal

## 2026-04-29 - Sensitive files tracked in Git
**Vulnerability:** Sensitive files like SQLite databases (`.db`) and application logs (`.log`) were being tracked in the Git repository.
**Learning:** Default `.gitignore` was insufficient, and these files had already been staged and committed, leading to potential exposure of trade data and internal logs.
**Prevention:** Always include `*.db` and `*.log` in `.gitignore` from the start and verify tracked files using `git ls-files`.
