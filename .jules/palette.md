## 2026-04-08 - Enhanced Data Visualization and Contextual Help
**Learning:** Using `st.column_config.ProgressColumn` for technical scores (0-100) significantly improves the ability to rapidly scan signal strength compared to raw numbers. Localizing tooltips while keeping technical headers in English/Mixed maintains consistency with existing UI patterns.
**Action:** Always prefer `ProgressColumn` for percentage-based or clamped 0-100 scores and use the `help` parameter to provide technical definitions for complex metrics.
