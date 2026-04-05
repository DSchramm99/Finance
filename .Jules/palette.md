## 2026-04-05 - Column Localization Synchronization
**Learning:** In Streamlit, when localizing `st.dataframe` headers via column renaming, any associated `st.column_config` keys and `column_order` lists must be updated to match the new localized strings exactly. Otherwise, the dataframe will fail to apply configurations or render the intended columns.
**Action:** Always verify that `column_config` and `column_order` are synchronized with renamed columns to prevent UI regressions.
