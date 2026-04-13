# Palette's UX Journal

## 2025-05-15 - Initial Audit
**Learning:** The application uses raw numbers for technical scores (Trend, Risk, Final) in a dataframe, which requires more cognitive load than visual indicators.
**Action:** Use `st.column_config.ProgressColumn` to visualize these scores on a 0-100 scale.
