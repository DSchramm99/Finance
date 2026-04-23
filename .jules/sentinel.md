## 2025-03-25 - [Exposed Sensitive Data in Repository]
**Vulnerability:** SQLite database files (`.db`) and system logs (`.log`) were being tracked by Git, potentially exposing sensitive trade data and internal application logs.
**Learning:** Adding patterns to `.gitignore` is insufficient if files are already part of the Git index. They must be explicitly removed using `git rm --cached` to stop tracking them while preserving local copies.
**Prevention:** Establish a pre-commit check or repository initialization standard that ensures local state and log files are not added to the initial commit, and proactively audit the index for binary or log files.
