# ThreatScope – Architecture Documentation

## High-Level Architecture

```mermaid
flowchart LR
    A[Threat Intel Feeds<br/>STIX/TAXII/MISP/OTX/VT/AbuseIPDB] --> B[Ingestion Service]
    B --> C[IOC Normalizer]
    C --> D[(PostgreSQL<br/>IOCs/Actors/Alerts)]
    C --> E[Elasticsearch<br/>Fast Search]
    E --> F[API Gateway<br/>FastAPI]
    F --> G[React Dashboard]
    F --> H[Correlation Engine]
    H --> I[Risk Scoring Engine]
    I --> J[Reporting Engine]
    K[Detection Rules<br/>Sigma/YARA] --> H
    L[MITRE ATT&CK<br/>Technique Library] --> H
    M[User / SOC Analyst] --> G
    M --> F
```

## Data Flow

```mermaid
sequenceDiagram
    participant TI as Threat Intel Source
    participant IN as Ingestion Service
    participant NM as IOC Normalizer
    participant DB as PostgreSQL
    participant ES as Elasticsearch
    participant CE as Correlation Engine
    participant RS as Risk Scorer
    participant API as API Layer
    participant UI as Dashboard

    TI->>IN: Push STIX bundle / Poll API
    IN->>NM: Raw indicators
    NM->>NM: Normalize schema
    NM->>DB: Persist structured IOCs
    NM->>ES: Index for search
    ES->>CE: Query related indicators
    CE->>CE: Cross-source correlation
    CE->>RS: Correlated indicators
    RS->>RS: Calculate risk score
    RS->>DB: Store risk assessments
    API->>DB: Fetch enriched IOCs
    API->>UI: Render investigation view
```

## Threat Intelligence Workflow

```mermaid
flowchart TD
    A[1. Collection] --> B[2. Normalization]
    B --> C[3. Deduplication]
    C --> D[4. Enrichment]
    D --> E[5. Correlation]
    E --> F[6. Scoring]
    F --> G[7. Alerting]
    G --> H[8. Investigation]
    H --> I[9. Response & Reporting]
```

## IOC Enrichment Workflow

```mermaid
flowchart LR
    A[Raw IOC] --> B{Type}
    B -->|IP| C[GeoIP + ASN + Reputation]
    B -->|Domain| D[WHOIS + DNS + Category]
    B -->|Hash| E[VirusTotal + MalwareBazaar]
    B -->|URL| F[URLScan + PhishTank]
    C --> G[Enriched IOC]
    D --> G
    E --> G
    F --> G
```

## Database Design

```mermaid
erDiagram
    IOC ||--o{ IOCSource : "has"
    IOC ||--o{ Correlation : "correlates"
    IOC ||--o{ Alert : "triggers"
    Actor ||--o{ Campaign : "conducts"
    Actor ||--o{ IOC : "attributed-to"
    Technique ||--o{ IOC : "maps-to"
    Technique ||--o{ DetectionRule : "covered-by"
    DetectionRule ||--o{ TechniqueCoverage : "covers"
    Report ||--o{ IOC : "references"
```

## API Design

- `POST /api/v1/ingest` — ingest STIX bundles or raw IOCs
- `GET /api/v1/iocs` — search and filter IOCs
- `POST /api/v1/iocs/{id}/enrich` — enrich a single IOC
- `POST /api/v1/correlate` — run correlation job
- `GET /api/v1/alerts` — list alerts with filters
- `POST /api/v1/score` — calculate risk score for indicators
- `GET /api/v1/mitre/coverage` — MITRE ATT&CK coverage matrix
- `POST /api/v1/sigma/convert` — convert Sigma rules to SIEM queries
- `POST /api/v1/yara/match` — match YARA rules against hashes
- `GET /api/v1/reports` — generate and retrieve reports
