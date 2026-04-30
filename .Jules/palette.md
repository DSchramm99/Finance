## 2026-04-30 - Enhanced Data Visualization in Stock Signals
**Learning:** Using `st.column_config.ProgressColumn` for abstract scores (like Trend or Risk) significantly improves scannability compared to raw numbers. Inverting risk into a "danger meter" (Risiko) where a fuller bar indicates higher volatility is more intuitive for users than a "stability score".
**Action:** Always prefer `ProgressColumn` for metrics on a fixed 0-100 scale and use `NumberColumn` with custom formatting for currencies and units.
