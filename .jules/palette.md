## 2025-05-01 - Progress Bars for Scannability
**Learning:** Using `st.column_config.ProgressColumn` for comparative metrics like Trend and Risk scores significantly improves scannability compared to plain numeric columns. However, inverting scores (e.g., 100 - risk_score) must be paired with precise tooltips to ensure the "fuller bar" correctly communicates the intended sentiment (e.g., higher volatility).
**Action:** Always verify that inverted metrics are accompanied by tooltips that explain whether a higher bar is "good" or "dangerous" to prevent user misinterpretation.
