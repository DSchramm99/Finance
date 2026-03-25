## 2025-03-05 - [Atomic Portfolio Updates]
**Vulnerability:** Race condition in portfolio capital updates.
**Learning:** Updating financial balances using a read-modify-write pattern (`SELECT`, then `UPDATE`) in Python is non-atomic and vulnerable to lost updates in concurrent environments.
**Prevention:** Always use atomic SQL statements like `UPDATE table SET column = column + ?` to ensure data integrity for sensitive state updates.
