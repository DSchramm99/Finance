## 2026-04-14 - Visual Progress Tracking for Trading Signals
**Learning:** Visualizing numerical scores (0-100) using `st.column_config.ProgressColumn` significantly reduces cognitive load compared to raw numbers, allowing for rapid signal strength assessment.
**Action:** Use ProgressColumn for all relative technical scores in Streamlit dataframes to improve at-a-glance readability.

## 2026-04-14 - Decoupling Data and Presentation Emojis
**Learning:** Embedding emojis directly in technical signal strings (e.g., in the strategy layer) is brittle and complicates data processing. Mapping emojis at the UI/presentation layer preserves data integrity while maintaining visual delight.
**Action:** Implement emoji enhancements using mapping dictionaries or custom formatters in the UI layer rather than modifying core business logic returns.
