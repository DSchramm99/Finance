## 2025-05-15 - Enhancing Trading Signals with Progress Bars
**Learning:** For scoring systems in trading dashboards, raw numerical values can be cognitively demanding. Using `st.column_config.ProgressColumn` in Streamlit provides an immediate visual representation of trend strength and risk, making it easier for users to compare opportunities at a glance.
**Action:** Always prefer visual indicators like progress bars or sparklines for performance and risk metrics to improve data scannability.

## 2025-05-15 - Interactive Documentation via Tooltips
**Learning:** In domain-specific applications like quantitative trading, technical terms (e.g., "Trend Score", "ATR Stop") can be ambiguous. Adding descriptive tooltips using the `help` parameter in `st.column_config` provides just-in-time documentation without cluttering the UI.
**Action:** Use header tooltips in data tables to explain the logic and importance of each column, especially for derived or calculated metrics.
