## 2025-03-05 - [Streamlit Data Visualization Enhancement]
**Learning:** Using `st.column_config` within `st.dataframe` allows for a much more intuitive and professional data presentation than simple `.style.format()`. Specifically, `ProgressColumn` provides immediate visual feedback for strength/risk scores (0-100), and `NumberColumn` with the `help` parameter enables localized technical explanations (tooltips) directly on table headers without cluttering the main UI.
**Action:** Always prefer `st.column_config` for financial tables to provide context (tooltips) and visual status (progress bars) for bounded metrics.

## 2025-03-05 - [Consistent Localization and UX Polish]
**Learning:** UX delight is diminished by linguistic inconsistency. Mixing English headers with German tooltips (or vice versa) creates cognitive friction. A unified language strategy across headers, tooltips, and form labels is essential for a professional and accessible interface.
**Action:** Ensure all user-facing strings (headers, tooltips, messages) in a specific component or view adhere to the same language to maintain interface coherence.
