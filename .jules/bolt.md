## 2025-05-15 - Identified Performance Bottlenecks
**Learning:** Initial profiling reveals two major bottlenecks: 1) Sequential ticker analysis in the signal generation loop, which takes ~75s for 30 tickers. 2) Extremely slow company name retrieval using `yf.Ticker(ticker).info`, which can take several seconds per call.
**Action:** Parallelize ticker scanning and implement a faster metadata retrieval method via the Yahoo Finance Search API.
