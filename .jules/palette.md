## 2026-03-25 - Dataframe Visual Indicators
**Learning:** Using raw numbers for scores (0-100) is less intuitive than visual progress bars in Streamlit dataframes. Combining `st.column_config.ProgressColumn` with `st.column_config.NumberColumn` (for currency/multipliers) provides a much denser and more readable information display.
**Action:** Always prefer `st.column_config` over `pandas.Styler` for numerical columns in Streamlit to ensure units and visual indicators are preserved and consistently rendered.
