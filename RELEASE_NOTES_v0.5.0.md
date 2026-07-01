# ThreatScope v0.5.0 — Release Notes

## Release Theme: Core Threat Intelligence Stack

This release delivers the minimal viable ThreatScope platform: ingestion, search, correlation, scoring, MITRE ATT&CK mapping, reporting, detection rules, auth/RBAC, and a frontend scaffold. It is suitable for local demos, portfolio use, and interview discussions.

## What's New

### Backend
- IOC ingestion endpoints: `/api/v1/ingest/raw` and `/api/v1/ingest/stix`
- IOC search and enrichment: `/api/v1/iocs/search` and `/api/v1/enrich/{id}/enrich`
- Correlation engine: `/api/v1/correlation/run`
- Risk scoring: `/api/v1/score`
- MITRE ATT&CK mapping: `/api/v1/mitre/search`, `/api/v1/mitre/{ioc_id}/map/{technique_id}`, `/api/v1/mitre/{ioc_id}`
- Reporting: `/api/v1/reports/ioc-summary`, `/api/v1/reports/threat-summary`
- Sigma/YARA rule management: `/api/v1/rules/` with validation endpoints
- Auth/RBAC scaffold: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me`
- Elasticsearch-backed search: `/api/v1/search/setup`, `/api/v1/search/index`, `/api/v1/search/query`
- Deterministic stable IOC IDs using normalized values
- Test coverage: pytest + ASGITransport for in-memory endpoint validation

### Infrastructure
- Docker Compose stack with healthchecks for Postgres, Elasticsearch, Redis, backend, and frontend
- Validation script: `scripts/validate_stack.sh`
- Dev setup script: `scripts/dev_setup.sh`
- Dockerfiles for backend and frontend
- `.env.example`

### Security and Compliance
- Role-based access with `viewer`, `analyst`, `admin`
- Pydantic schema validation on all primary endpoints
- SECURITY.md with reporting policy
- Bandit scaffold in CI

### Frontend
- React + TypeScript + Vite scaffold
- Dashboard page with IOC summary KPIs and type distribution
- IOC investigation page with tabular search results

### DevOps
- GitHub Actions CI with lint, tests, Docker build, and security scan
- Dependency review workflow
- Pre-commit hooks for Ruff and Bandit
- Makefile for common developer tasks
- EditorConfig and Gitpod workspace config

### Documentation
- README with feature overview, tech stack, API docs, and roadmap
- Architecture docs with Mermaid diagrams
- Interview prep scaffold with technical and HR questions

## How to Run

```bash
git clone git@github.com:GodSpell28/ThreatScope.git
cd ThreatScope
cp docker/.env.example .env
docker compose up --build
```

Backend: `http://localhost:8000`
Frontend: `http://localhost:5173`

## Known Limitations in v0.5.0

- Auth is a demo implementation; real password hashing and JWT verification are not enabled
- External threat-intelligence enrichment is placeholder-only
- No async queue workers yet
- No Kibana dashboards beyond Elasticsearch index scaffold
- No PDF/CSV export, only JSON reports

## Roadmap to v1.0.0

- Real JWT auth and refresh tokens
- Async ingestion pipeline with Redis/RabbitMQ
- Expanded enrichment integrations (VirusTotal, AbuseIPDB, OTX, MISP)
- Kibana dashboards for investigations
- Full React UI with investigation and reporting workflows
- PDF/CSV report export
- Sigma-to-SIEM conversion
- YARA runtime matching
- Rate limiting and audit logging
