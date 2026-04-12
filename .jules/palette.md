## 2024-04-10 - Streamlit ProgressColumn & Emojis
**Learning:** Using `st.column_config.ProgressColumn` significantly improves the scannability of technical scores compared to raw numbers. Adding emojis to categorical labels (like signals) provides instant visual cues and "delight" without sacrificing clarity, provided that backend logic (like styling) is updated to handle the new strings via substring matching.
**Action:** Always prefer native Streamlit column configurations over raw dataframes for technical indicators, and ensure styler functions are robust against string modifications.
