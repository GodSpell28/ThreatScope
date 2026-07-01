# ThreatScope

![Security](https://img.shields.io/badge/security-portfolio-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.114.2-green)

![Architecture](architecture/ARCHITECTURE.md)

ThreatScope is a **Cyber Threat Intelligence & IOC Correlation Platform** built for portfolio-ready demonstration, interview preparation, and real-world SOC/CTI workflows. It ingests indicators, enriches context, correlates related IOCs, maps to MITRE ATT&CK, scores risk, supports Sigma/YARA rules, and exposes an investigation-ready backend with a React frontend scaffold.

## What it demonstrates

- IOC ingestion, normalization, and deduplication
- Search, enrichment, and correlation workflows
- MITRE ATT&CK technique mapping
- Risk scoring engine
- Reporting: IOC summaries and technique coverage
- Sigma/YARA rule ingestion and lightweight validation
- Role-based access with scoped auth
- Elasticsearch-backed IOC search scaffold
- Docker Compose dev runtime with healthchecks
- CI workflow with lint, test, build, and security scan

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | FastAPI + Uvicorn + Pydantic v2 |
| Auth | Demo JWT-style tokens with role scopes |
| ORM / DB | SQLAlchemy + PostgreSQL 15 |
| Search | Elasticsearch 8 + mappings for IOCs |
| Cache / Queue | Redis scaffold |
| Frontend | React 18 + TypeScript + Vite |
| Containerization | Docker + Docker Compose |
| CI | GitHub Actions |

## Repository Structure

```text
ThreatScope/
backend/
  app/
    routers/
    models/
    schemas/
    services/
  scripts/
frontend/
infrastructure/
tests/
scripts/
sample_data/
screenshots/
architecture/
dashboards/
sigma/
yara/
reports/
docker/
.github/workflows/
docs/
README.md
LICENSE
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Node.js 18+ for frontend development

### Run with Docker

```bash
git clone git@github.com:GodSpell28/ThreatScope.git
cd ThreatScope
cp docker/.env.example .env
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Elasticsearch: `http://localhost:9200`
- PostgreSQL: `localhost:5432`

## Backend Quickstart

```bash
cd backend
pip install -r ../backend/requirements.txt
uvicorn app.main:app --reload
```

## Seed Data

```bash
cd backend
python scripts/seed_mitre.py --reset
python scripts/seed_elasticsearch.py --reset
```

## API Overview

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/ingest/raw` | Ingest normalized IOCs |
| GET | `/api/v1/iocs/search` | Search and filter IOCs |
| POST | `/api/v1/enrich/{id}/enrich` | Enrichment workflow |
| GET | `/api/v1/correlation/run` | Run IOC correlation |
| GET/POST | `/api/v1/score` | Risk scoring |
| GET/POST | `/api/v1/mitre/search` | Search MITRE techniques |
| POST | `/api/v1/mitre/{ioc_id}/map/{technique_id}` | Map IOC to technique |
| GET | `/api/v1/reports/ioc-summary` | IOC summary report |
| GET | `/api/v1/reports/threat-summary` | Technique coverage report |
| POST/GET | `/api/v1/rules/` | Sigma/YARA rule management |
| POST | `/api/v1/rules/{id}/validate` | Validate rule syntax |
| GET | `/api/v1/search/query` | Elasticsearch-backed IOC search |
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Obtain access token |
| GET | `/api/v1/auth/me` | Current user profile |

## Frontend Pages

- `/` — Dashboard with IOC KPIs and type distribution
- `/iocs` — IOC investigation table

## Security Considerations

- Role-based access: `viewer`, `analyst`, `admin`
- Token-scoped endpoint protection
- Input validation with Pydantic
- Rate limiting scaffold
- Audit considerations documented in `SECURITY.md`

## Detection Engineering

- Sigma rules can be stored and validated
- YARA rules can be stored and validated
- Rules are intended for future SIEM/malware pipeline integration

## Testing

```bash
pytest tests/
```

## Roadmap

- [ ] Replace demo auth with real password hashing and JWT verification
- [ ] Async ingestion workers and queue-based pipeline
- [ ] Expanded enrichment integrations
- [ ] Kibana dashboards for threat investigation
- [ ] Full React investigation and reporting UI
- [ ] PDF/CSV report export
- [ ] Sigma-to-SIEM conversion utilities
- [ ] YARA runtime matching workflow
- [ ] Rate limiting and audit logging

## License

MIT — see `LICENSE`

## Author

Built by [GodSpell28](https://github.com/GodSpell28)
