# Sentinel's Journal - Critical Security Learnings Only

This journal is used to record critical security learnings discovered during the protection of the codebase.

Format:
## YYYY-MM-DD - [Title]
**Vulnerability:** [What you found]
**Learning:** [Why it existed]
**Prevention:** [How to avoid next time]

## 2026-03-25 - Hardening Repository and Network Requests
**Vulnerability:** Sensitive files including SQLite databases (`trading_live.db`, etc.) and a system log (`streamlit.log`) containing internal IP addresses were committed to the repository. Additionally, network requests were lacking timeouts.
**Learning:** Default `.gitignore` was too permissive, and standard library `requests` does not have a default timeout, which can lead to hanging processes.
**Prevention:** Always use `*.db` and `*.log` in `.gitignore`. Mandate `timeout` parameter for all `requests` calls.
