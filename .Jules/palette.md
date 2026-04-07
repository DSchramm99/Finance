## 2025-05-15 - ProgressColumn for Technical Scores
**Learning:** For bounded metrics (0-100) such as Trend or Risk scores in Streamlit DataFrames, `st.column_config.ProgressColumn` is the preferred UI pattern for quick visual interpretation.
**Action:** Use ProgressColumn for any numerical technical score within Streamlit data tables to allow users to rapidly assess signal strength without reading raw numbers.

## 2025-05-15 - Contextual Tooltips for Financial Metrics
**Learning:** `st.column_config.NumberColumn` (and other column configs) with the `help` parameter is the standard for providing contextual explanations for technical financial metrics (ATR multipliers, Chandelier stops) in Streamlit data tables.
**Action:** Always provide localized (German) help tooltips for technical trading terms to improve accessibility for non-expert users.
