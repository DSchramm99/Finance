## 2025-03-25 - Safe Company Name Fetcher
**Vulnerability:** Use of yf.Ticker(ticker).info without timeouts could cause DoS-like hangs in the Streamlit UI.
**Learning:** The Yahoo Finance API via yfinance can be unreliable and block indefinitely on metadata calls.
**Prevention:** Use direct Yahoo Finance Search API calls with explicit timeouts and generic error messages.
