## 2025-05-15 - Modernized Signals Visualization and Contextual Safety

**Learning:** Streamlit `st.dataframe` with `column_config` provides a much cleaner UX for technical scores than raw numbers. Using `ProgressColumn` for normalized scores (0-100) allows for instant visual ranking without cognitive load. Emojis in status columns (like "✅ BUY") significantly improve scanability compared to plain text.

**Action:** Always prefer `st.column_config` over `pandas.Styler` for formatting in modern Streamlit apps, and use `ProgressColumn` for any normalized strength/risk metrics. Combine icons with text in status fields to leverage both visual and semantic cues.
