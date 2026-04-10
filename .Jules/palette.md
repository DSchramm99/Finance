## 2026-04-10 - Streamlit ProgressColumn for Scoring
**Learning:** Using `st.column_config.ProgressColumn` for numeric scores (0-100) significantly improves scannability compared to raw numbers, allowing users to rapidly assess trade signal strength.
**Action:** Prefer `ProgressColumn` for any bounded technical indicators or scores in data tables.

## 2026-04-10 - Destructive Action Tooltips
**Learning:** Adding the `help` parameter to buttons that perform irreversible actions (like database resets or deletions) provides a low-friction safety net without requiring intrusive confirmation dialogs for every micro-action.
**Action:** Always include a warning in `help` tooltips for any "Delete" or "Reset" functionality.
