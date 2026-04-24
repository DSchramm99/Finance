## 2025-05-15 - Streamlit Popover Selector Conflict in Playwright
**Learning:** When using `st.popover` in Streamlit, Playwright's `get_by_text` can trigger strict mode violations because the label text often appears twice in the DOM (once for the button and once inside the popover structure).
**Action:** Use `.first` or `.nth(0)` when targeting Streamlit popover triggers by text, or use more specific ARIA role selectors if available to avoid ambiguity.
