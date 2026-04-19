## 2026-03-25 - Prevent DoS hangs via network timeouts
**Vulnerability:** Application instability and potential Denial of Service (DoS) due to missing timeouts in network requests (Wikipedia scraping and metadata retrieval).
**Learning:** Using `yf.Ticker(ticker).info` is slow and unreliable for bulk metadata retrieval. The Yahoo Finance Search API (`query2.finance.yahoo.com/v1/finance/search`) is a faster, more specific alternative.
**Prevention:** Implement mandatory 10-second timeouts for all `requests.get()` calls and use the `params` argument for secure URL encoding.
