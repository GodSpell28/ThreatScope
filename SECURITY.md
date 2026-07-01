# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | Yes                |
| 0.9.x   | Security fixes only |
| < 0.9   | No                 |

## Reporting a Vulnerability

ThreatScope is an open-source portfolio project. If you find a security issue, please report it responsibly.

### Reporting Process
1. Email: **security@example.com** (replace with your preferred contact)
2. Subject: `[ThreatScope] Vulnerability Report`
3. Include:
   - Summary of the vulnerability
   - Affected version/component
   - Steps to reproduce
   - Proof of concept if safe to share
   - Suggested fix if available

### Response Timeline
- Acknowledgment within **48 hours**
- Assessment and triage within **7 days**
- Fix timeline depends on severity:
  - Critical: **14 days**
  - High: **30 days**
  - Medium/Low: Next release cycle

### Out of Scope
- Issues in third-party dependencies
- Theoretical vulnerabilities without working POC
- Issues requiring physical access
- Social engineering against maintainers

## Security Controls

See [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md) for:
- Authentication and authorization design
- Rate limiting approach
- Input validation strategy
- Secrets management
- Audit logging

Thank you for helping keep ThreatScope secure.
