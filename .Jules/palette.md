## 2025-01-24 - [Actionable Empty States]
**Learning:** In complex trading applications, empty dashboard states (like an empty portfolio) can be dead ends for new users. Adding a clear Call-to-Action (CTA) that links directly to the primary data generation tool (the scanner) significantly improves the onboarding flow.
**Action:** Always include a CTA in empty state messages that directs users to the next logical step in the application workflow.

## 2025-01-24 - [Visualizing Risk and Performance]
**Learning:** Raw numeric scores (0-100) are hard to scan quickly in large tables. Using visual progress bars makes it easier to identify outliers. Furthermore, "Risk" is more intuitively understood when higher bars represent higher risk, even if the underlying model uses "100 - score" for volatility.
**Action:** Use `st.column_config.ProgressColumn` for relative metrics and ensure the visual representation (filling of the bar) matches the user's mental model of "higher is more".
