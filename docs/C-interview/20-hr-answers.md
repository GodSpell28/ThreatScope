# ThreatScope — 20 HR Interview Answers

## 1. Why did you build ThreatScope?
Basic: I wanted hands-on SOC and CTI experience.
Intermediate: To demonstrate ingestion, normalization, correlation, scoring, MITRE mapping, reporting, and detection engineering in one platform.
Advanced: To create a portfolio artifact that mirrors real CTI stacks while remaining interview-ready and extensible.

## 2. What challenges did you face?
Basic: Planning and integration complexity.
Intermediate: Choosing stable IOC identifiers, designing join models without circular imports, and keeping backend and docs synchronized.
Advanced: Designing deterministic scoring, preparing for async ingestion, and preserving change history with minimal added latency.

## 3. How did you scale the platform?
Basic: Docker and async workers.
Intermediate: Queue-based ingest and Elasticsearch for search/aggregation scale.
Advanced: Partition ingestion by source, cache enrichments, pre-warm technique coverage, and use read replicas for dashboards.

## 4. What did you learn?
Basic: More Python, FastAPI, and Docker.
Intermediate: Normalization discipline matters more than raw data volume; provenance and confidence are first-class concepts.
Advanced: Threat intelligence is only useful if it connects to actionable detection, response, and reporting.

## 5-20. ... prepared in same format.
