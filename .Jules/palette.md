## 2026-04-27 - Streamlit Playwright Selection
**Learning:** When using Playwright to verify Streamlit apps, text-based selectors can often cause strict mode violations (multiple elements found) because Streamlit may render the same text in both a button and its internal labels or popovers.
**Action:** Use `.first` or more specific selectors like `get_by_role(button, name=...)` when targeting interactive elements in Streamlit.
