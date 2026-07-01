# GitHub Repository Description

ThreatScope is a Cyber Threat Intelligence & IOC Correlation Platform built with FastAPI, React, PostgreSQL, and Elasticsearch. It demonstrates end-to-end SOC/CTI workflows: IOC ingestion, normalization, deduplication, enrichment, correlation, risk scoring, MITRE ATT&CK mapping, reporting, and detection rule management.

## Key Features
- IOC ingestion with stable IDs and provenance
- Search, enrichment, and correlation endpoints
- Weighted risk scoring engine
- MITRE ATT&CK technique mapping and coverage reports
- Sigma/YARA rule management and validation
- Role-based access with scoped permissions
- Elasticsearch-backed IOC search
- React + TypeScript dashboard scaffold
- Docker Compose dev runtime with healthchecks
- CI with lint, tests, Docker validation, and security scanning
- Comprehensive interview and documentation package

## Quick Start
```bash
git clone git@github.com:GodSpell28/ThreatScope.git
cd ThreatScope
cp docker/.env.example .env
docker compose up --build
```

Backend: http://localhost:8000
Frontend: http://localhost:5173

Built by [GodSpell28](https://github.com/GodSpell28)
