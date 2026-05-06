## 2026-05-04 - Visual scoring in Streamlit
**Learning:** Using `st.column_config.ProgressColumn` with `color='auto'` or `color='auto-inverse'` significantly improves the scannability of numeric scores compared to raw numbers. Inverting the 'Risk Score' into a 'Risk (Danger)' metric where a fuller bar indicates more risk (using `auto-inverse`) is more intuitive for users than a 'stability' score.
**Action:** Always prefer `ProgressColumn` for metrics on a fixed 0-100 scale, and consider if the metric should be inverted to align with 'higher is more intense' visual logic.
