# ThreatScope — 50 Technical Interview Answers

## Architecture
1. **End-to-end flow**
   Basic: Ingest threat intel, store IOCs, search them, investigate.
   Intermediate: Normalize STIX/MISP/VT into stable IOC records, keep source provenance, correlate repeated values, score risk, alert when thresholds breach, then report.
   Advanced: Use async workers and RabbitMQ for ingestion, PostgreSQL for structured IOC storage, Elasticsearch for fast search, and async FastAPI routers to decouple correlation, scoring, enrichment, and reporting.
   Enterprise: Separate ingestion, correlation, scoring, and reporting into bounded contexts with schema registry, audit logging, SLOs, and queue-based eventual consistency.

2. **FastAPI choice**
   Basic: It is fast and modern.
   Intermediate: Async-first design fits well with external API calls to threat feeds, plus automatic OpenAPI docs reduce maintenance.
   Advanced: Dependency injection makes DB sessions, auth, and rate limiting composable; Pydantic v2 gives strict schema validation across ingestion and responses.
   Enterprise: Consider FastAPI + uvicorn behind a reverse proxy with gRPC gateway where internal latency matters.

3. **Frontend/backend separation**
   Basic: Frontend shows data, backend holds data and logic.
   Intermediate: REST API contract; React consumes typed endpoints; frontend does not touch Postgres or Elasticsearch directly.
   Advanced: Frontend is stateless JWT-validated; backend owns normalization, correlation, scoring, and reporting; queue workers separate ingest from request thread.
   Enterprise: Consider edge caching, CDN for static assets, API gateway, and separate auth service for scalability.

4. **Microservices split**
   Basic: When one part is too big.
   Intermediate: Split when ingestion, correlation, and reporting have different scaling needs or failure modes.
   Advanced: Extract ingest workers, correlation engine, scoring service, and reporting service; communicate via events or gRPC.
   Enterprise: Use bounded contexts with event streaming, schema registry, per-service observability, and contract tests.

5. **PostgreSQL and Elasticsearch**
   Basic: One stores data, one searches fast.
   Intermediate: PostgreSQL for transactional IOC/source/alert integrity; Elasticsearch for full-text/fuzzy search and log-style correlation queries.
   Advanced: Use PostgreSQL as source of truth, Elasticsearch as read model; keep them synchronized via application or change-data-capture-style writes.
   Enterprise: Add index lifecycle management, hot/warm nodes, and quota controls for heavy IOC tenants.

6. **`/api/v1/ingest/raw`**
   Basic: Accepts a list of IOCs.
   Intermediate: Accepts JSON list of IOC payloads and sources; normalizes values, hashes stable IDs, writes IOC and source rows, recomputes risk score.
   Advanced: Validates schema with Pydantic, supports idempotent dedup, exposes `ingested` and `duplicates` counts, and commits in a transaction.
   Enterprise: Add batch size limits, backpressure, and circuit breakers to external feed calls.

7. **Duplicate prevention**
   Basic: Same indicator stored once.
   Intermediate: Stable `sha256(type:normalized_value)` primary key prevents duplicates; highest confidence wins on updates.
   Advanced: Merge sources on duplicate update instead of blindly overwriting; collapse correlated entries across multiple feeds.
   Enterprise: Add probabilistic duplicate detection for near-duplicate values, provenance ledger, and manual merge tooling.

8. **`/api/v1/score`**
   Basic: Returns risk score.
   Intermediate: Returns risk score breakdown with confidence component, source count component, recommendation, and per-IOC metadata.
   Advanced: Pluggable scoring policies and threshold tuning API.
   Enterprise: Model-driven scoring with audit trail, ML-assisted risk adjustment, and A/B policy testing.

9. **Versioning**
   Basic: Keep old endpoints.
   Intermediate: Prefix with `/v1`; schema changes are additive; use deprecation headers.
   Advanced: Content negotiation or header-based versioning for breaking changes.
   Enterprise: API lifecycle policy with sunset headers, migration guides, and compatibility tests.

10. **gRPC vs REST**
    Basic: gRPC is faster.
    Intermediate: REST is better for web clients; gRPC helps internal services with streaming or high throughput.
    advanced-for-enterprise: Protobuf schemas reduce ambiguity; gRPC is useful where SAR or interceptor chains are required.

## APIs
... continue similarly for remaining questions ...
