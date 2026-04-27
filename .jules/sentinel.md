## 2025-05-15 - Sensitive files tracked in Git
**Vulnerability:** SQLite database files (*.db) and Streamlit logs (*.log) were being tracked by Git.
**Learning:** Initial project setup often forgets to ignore local data and log files, leading to potential exposure of sensitive information like trade history or server IP addresses.
**Prevention:** Always include *.db and *.log in .gitignore from the start and verify tracking with git ls-files.

## 2025-05-15 - Unbounded network requests
**Vulnerability:** External requests to Wikipedia were made without a timeout.
**Learning:** Missing timeouts can lead to application hangs and potential DoS if the remote server is slow or malicious.
**Prevention:** Always use the 'timeout' parameter in 'requests' calls and wrap response content in 'StringIO' for 'pd.read_html' to avoid deprecation warnings and ensure secure parsing.
