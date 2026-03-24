# Sentinel Journal

## 2025-05-22 - Non-Atomic Database Updates
**Vulnerability:** Race condition in portfolio capital updates.
**Learning:** The `close_trade` function was reading the capital, modifying it in Python, and writing it back. This is not thread-safe or process-safe in a multi-user environment (like a Streamlit app).
**Prevention:** Use atomic SQL `UPDATE` statements (e.g., `SET capital = capital + ?`) to ensure consistency during concurrent updates.
