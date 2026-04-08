# Sentinel Journal - Security Learnings

## 2026-04-08 - Network Reliability and Information Leakage
**Vulnerability:** Missing timeouts on network requests (`requests.get`, `yf.download`) and exposure of raw exception messages in the UI.
**Learning:** Default configurations often prioritize convenience over robustness, leading to potential DoS through hung requests and information leakage through verbose errors.
**Prevention:** Enforce mandatory timeouts for all external calls and sanitize all user-facing error messages to use generic descriptions.
