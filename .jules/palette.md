## 2025-05-15 - [Confirmation Popovers in Streamlit]
**Learning:** Using `st.popover` for confirmation dialogs in Streamlit provides a clean, low-overhead way to prevent accidental destructive actions without the state-management complexity of custom modal components.
**Action:** Prefer `st.popover` with a primary-type "Confirm" button for any non-reversible user actions.
