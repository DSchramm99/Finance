## 2024-04-16 - [Streamlit Dataframe Visualization]
**Learning:** Using `st.column_config.ProgressColumn` for scoring metrics significantly improves the immediate scannability of trade opportunities compared to raw numbers. Additionally, for destructive actions, `st.popover` provides a lightweight and accessible confirmation pattern that fits naturally into the Streamlit flow.
**Action:** Prioritize `st.column_config` over `Styler.format` for complex numerical display in Streamlit to avoid formatting conflicts and leverage native UI components like progress bars.

## 2024-04-16 - [Defensive Row Styling]
**Learning:** When using `st.dataframe.style.apply`, always use bracket notation `row['ColumnName']` instead of dot notation `row.ColumnName`. Renamed columns or those with technical names can easily cause `AttributeError` or `KeyError` if dot notation is used after a `.rename()` operation.
**Action:** Adopt bracket notation as the default standard for all Streamlit styling helper functions.
