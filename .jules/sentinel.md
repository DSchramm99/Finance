## 2025-05-22 - Missing Request Timeouts
**Vulnerability:** Potential Denial of Service (DoS) due to indefinite hangs in network requests.
**Learning:** External data fetching from Wikipedia via `requests.get` lacked a timeout, which could cause the entire application (including the Streamlit UI) to hang if the server is unresponsive.
**Prevention:** Always specify a `timeout` parameter in `requests` calls to ensure the application fails gracefully.
