## 2024-05-21 - Denial of Service (DoS) via Blocking Network Requests
**Vulnerability:** The application performed network requests without timeouts and used the blocking `yf.Ticker.info` method, which can lead to application hangs and resource exhaustion.
**Learning:** External API calls (like Wikipedia scraping and Yahoo Finance) are unpredictable. Without explicit timeouts, a single slow response can block the main execution thread or Streamlit session.
**Prevention:** Always implement a mandatory timeout (e.g., 10 seconds) for all network requests. Use lightweight API endpoints (like Yahoo Finance Search) instead of heavy metadata calls like `.info` for simple data like company names.
