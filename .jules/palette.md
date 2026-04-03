## 2026-04-03 - Enhancing Financial Data Visibility with Streamlit Column Config

**Learning:** Using `st.column_config.ProgressColumn` for bounded scores (0-100) provides an immediate visual "strength" indicator that is more intuitive than raw numbers for trading signals. However, localizing DataFrames via column renaming requires strict synchronization with `column_order` and `column_config` keys; any mismatch leads to columns silently disappearing from the UI.

**Action:** Always verify that renamed columns in `st.dataframe` are reflected in all configuration dictionaries and ordering lists. Use unique scoped variables for column lists (e.g., `display_cols_mon`) to prevent regressions during multi-step styling or renaming processes.
