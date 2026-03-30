## 2025-05-14 - Visual Progress Bars and Tooltips
**Learning:** For financial applications with multiple technical scores (0-100), using `st.column_config.ProgressColumn` significantly reduces cognitive load by allowing users to scan relative strengths visually rather than parsing numbers. Tooltips in headers are essential for explaining complex domain terms (ATR, Chandelier stops) without cluttering the UI.
**Action:** Use `ProgressColumn` for bounded scores and `NumberColumn` with `help` text for technical metrics in all future Streamlit data tables.
