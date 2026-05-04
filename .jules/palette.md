## 2025-05-15 - Improving scanability of numeric scores in Streamlit
**Learning:** For numeric metrics like 'Trend' and 'Risk' (0-100), using `st.column_config.ProgressColumn` with `format='%d'` significantly improves scannability compared to plain numbers, turning data into a visual 'danger meter'.
**Action:** Use ProgressColumn for any 0-100 score that represents a state or intensity, and ensure English tooltips are provided for better accessibility in financial dashboards.
