# ThreatScope — ATS-Friendly Resume Points

## Beginner Version
- Built a Python-based Threat Intelligence & IOC Correlation Platform (ThreatScope) using FastAPI, SQLAlchemy, and React.
- Implemented IOC ingestion, search, and basic correlation to demonstrate SOC and CTI workflow understanding.
- Added MITRE ATT&CK technique mapping and risk scoring to support analyst prioritization.
- Created pytest-based API tests and Docker Compose runtime for reproducible demos.

## Intermediate Version
- Designed and developed a full-stack threat intelligence platform with REST APIs for ingestion, enrichment, correlation, scoring, MITRE mapping, reporting, and Sigma/YARA rule management.
- Built role-based access control with scoped permissions (viewer, analyst, admin) and JWT-style authentication.
- Integrated Elasticsearch for IOC search with dedicated mappings, plus seed scripts for MITRE ATT&CK data and sample IOC documents.
- Established CI/CD with GitHub Actions covering lint, tests, Docker build validation, and security scanning (Bandit).

## Advanced Version
- Architected a portfolio-grade CTI platform demonstrating end-to-end SOC capability: ingestion normalization, deduplication, provenance tracking, IOC correlation, weighted risk scoring, MITRE coverage analytics, JSON reporting, and detection rule validation.
- Implemented production-leaning backend patterns: Pydantic v2 schema validation, SQLAlchemy ORM with stable hash-based IDs, async-ready FastAPI routers, and service-layer separation.
- Delivered frontend scaffold (React + TypeScript + Vite) with dashboard KPIs and IOC investigation tables, plus Docker Compose healthchecks and validation scripts.
- Prepared comprehensive interview documentation: 50 technical questions, 20 HR questions, architecture diagrams, and a tagged v0.5.0 release suitable for SOC Analyst, Threat Intelligence Analyst, and Detection Engineer roles.
