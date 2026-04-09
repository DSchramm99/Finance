# Palette Journal

## 2025-05-15 - Visualizing Signals with Emojis
**Learning:** Adding emojis to status strings (e.g., "BUY 🚀") improves immediate visual recognition but breaks exact-match styling logic.
**Action:** Always use substring matching (e.g., `if "BUY" in str(row["Signal"])`) in styler functions when using emojis in dataframes.

## 2025-05-15 - Streamlit Data Visualization
**Learning:** `st.column_config.ProgressColumn` is much more intuitive than raw numbers for scoring metrics (0-100), as it allows users to scan relative strengths instantly.
**Action:** Use ProgressColumn for all normalized technical scores in the UI.
