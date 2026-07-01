# Section C – Interview Preparation

This document gives answer sets across three levels for common SOC, threat intelligence, detection engineering, and software architecture interviews using ThreatScope as the primary project example.

Format:
- **Question**
- Basic — short, conceptual, beginner-friendly
- Intermediate — implementation-aware, SOC-relevant
- Advanced — architecture/scale/incident-response oriented

---

## 50 Technical Interview Questions

### Architecture

1. What is ThreatScope?
- **Basic:** ThreatScope is a Python project that collects threat indicators, stores them, searches them, and shows which MITRE techniques they relate to.
- **Intermediate:** It is a FastAPI-based backend with PostgreSQL, Elasticsearch, and Redis for IOC ingestion, search, enrichment, correlation, risk scoring, MITRE mapping, reporting, and Sigma/YARA rule management.
- **Advanced:** ThreatScope is designed as a modular threat intelligence platform with async-capable services, multiple enrichment sources, correlation layer, risk scoring engine, detection coverage reporting, RBAC, and CI-hardened packaging for portfolio/documentation use.

2. Why FastAPI instead of Flask or Django?
- **Basic:** FastAPI is modern and easy to build APIs with.
- **Intermediate:** It provides async support, automatic OpenAPI docs, request validation with Pydantic, and dependency injection, which fit security tooling workloads well.
- **Advanced:** FastAPI reduces boilerplate for REST endpoints, integrates well with async DB clients and queues, and produces typed API docs beneficial for integration with SIEMs and automation pipelines.

3. Why PostgreSQL over MongoDB?
- **Basic:** PostgreSQL stores structured data well.
- **Intermediate:** Strong typing, indexes, foreign keys, and SQLAlchemy ORM suit normalized threat intel data, relationships between IOCs and techniques, and analytics.
- **Advanced:** ACID consistency matters for threat data lifecycle, auditability, and deterministic correlation joins. SQL is also more familiar to enterprise SIEM teams.

4. Why Elasticsearch here?
- **Basic:** To search IOC data fast.
- **Intermediate:** Elasticsearch supports full-text search, flexible queries, and aggregations for dashboards and investigations.
- **Advanced:** In production, ES complements PostgreSQL when datasets grow large; it delivers near-real-time search and faceting across threat feeds.

5. How would you scale ThreatScope?
- **Basic:** Add more servers and a load balancer.
- **Intermediate:** Horizontal REST nodes, partitioned queues (RabbitMQ/Kafka), separate write/read DB nodes, and cluster Elasticsearch.
- **Advanced:** Introduce event-driven ingestion, partition storage by time/family, caching via Redis, rate limiting, multi-tenant routing, and circuit breakers for external TI sources.

### APIs

6. What does `/api/v1/ingest/raw` do?
- **Basic:** Accepts a list of IOC items to save.
- **Intermediate:** Normalizes values, deduplicates by stable SHA-based `id`, updates confidence on duplicates, creates source provenance entries, and computes risk scores.
- **Advanced:** It exposes an idempotent ingestion contract—safe to call repeatedly without proliferating duplicates—solvable by deterministic IDs and merge logic.

7. What does `/api/v1/iocs/search` support?
- **Basic:** Search IOCs by text, type, risk threshold, and limit.
- **Intermediate:** It returns ordered results and can be integrated into a frontend investigation panel.
- **Advanced:** Enterprise enhancement would include pagination, facets, export, saved searches, RBAC-scoped access, audit logging of query context, and policy actions.

8. How do you secure API endpoints?
- **Basic:** Usernames and passwords with tokens.
- **Intermediate:** JWT plus role-based scopes (`viewer`, `analyst`, `admin`) so endpoints like IOC search enforce `iocs:read`.
- **Advanced:** Add refresh tokens, short-lived access tokens, token revocation, mTLS for backend services, WAF policies, IP allowlisting, anomaly detection on API usage, and structured audit logs.

9. How is data validated?
- **Basic:** JSON schema checks via Pydantic.
- **Intermediate:** Request/response models enforce structure and types, rejecting malformed IOCs at ingest boundaries.
- **Advanced:** Add regex allowlists for indicator formats, schema validation for STIX bundles, content safety checks, and sanitization to prevent injection in storage or downstream SIEM queries.

10. What is an idempotent ingestion API and why is it important?
- **Basic:** Sending the same data twice should not create duplicates.
- **Intermediate:** Deterministic `id = sha256(type:value)` lets merge-on-update behavior collapse repeated uploads while preserving highest-confidence sources.
- **Advanced:** Idempotency matters for TI feeds that retry, enabling safe pipelines, replay debugging, and consistent state across distributed ingestion workers.

### Databases

11. How is uniqueness enforced for IOCs?
- **Basic:** IOC values have a unique index in SQLAlchemy.
- **Intermediate:** Additionally, stable IDs ensure dedup and update safe operations through `db.get` and merge logic.
- **Advanced:** Database uniqueness is a guard, but logical dedup handles case normalization, type-specific parsing, and source-aware merging beyond simple unique constraints.

12. How do you handle schema evolution?
- **Basic:** Add new tables or columns carefully.
- **Intermediate:** Use Alembic migrations to version database schema changes and support rollback.
- **Advanced:** Maintain backwards-compatible contracts for SaaS consumers, allow dual-write during migration, and test schema changes against production-like fixtures.

13. When would you prefer Elasticsearch over PostgreSQL for a query?
- **Basic:** When you want fast text search across many indicators.
- **Intermediate:** Aggregations on risk scores, facets on type or source, or fuzzy matching for analyst UI autocomplete.
- **Advanced:** ES is better for wide-time-range threat hunt queries and dashboard aggregations; PostgreSQL remains the source of truth for relational accuracy and join integrity.

14. What indexes do you consider important?
- **Basic:** Indexes on `type`, `value`, and `risk_score`.
- **Intermediate:** Composite indexes on commonly filtered fields and partial indexes for high-risk rows.
- **Advanced:** Covering indexes for read-heavy endpoints, GIN indexes for text patterns, partitioned indexes by ingest date for older data, and ES mappings optimized for aggregations.

### Threat Intelligence

15. What is an IOC?
- **Basic:** Indicator of Compromise. Something like an IP, domain, URL, or file hash.
- **Intermediate:** A normalized entity with confidence, sources, risk score, timestamps, and mappings used for detection and investigation.
- **Advanced:** IOCs are temporal and probabilistic evidence, not binary truth. Real-world usage requires provenance, confidence decay handling, and risk scoring because raw feeds contain stale, conflicting, or deliberately planted data.

16. Why store sources for each IOC?
- **Basic:** To know where it came from.
- **Intermediate:** Source metadata supports trust weighting, deduplication, feed health, and enrichment lineage.
- **Advanced:** Provenance enables audit reporting, source reliability analysis, and corpus filtering for regulatory or organizational trust boundaries.

17. What is risk scoring?
- **Basic:** A number reflecting how dangerous an indicator is.
- **Intermediate:** It combines source confidence, number of sources, and correlation strength.
- **Advanced:** Risk scoring should factor source reputation, historical prevalence, exploitation activity, threat actor attribution, affected asset criticality, and business context. Treat it as tunable policy rather than an absolute score.

18. What is correlation in threat intel?
- **Basic:** Finding related indicators.
- **Intermediate:** Grouping IOCs that share values or attributes across sources and time windows.
- **Advanced:** Correlation should use temporal windows, behavioral joins (file-hash-to-domain, IP-to-ASN), graph-based relationships, and rule-driven alerting with confidence weighting to reduce false positives.

### IOC Enrichment

19. What does IOC enrichment mean?
- **Basic:** Adding extra information about an indicator, like its location or reputation.
- **Intermediate:** External lookups for geolocation, ASN, WHOIS, passive DNS, VT scores, categories, and metadata.
- **Advanced:** Enrichment is a data lineage concern. Each enrichment source must have latency, quota, freshness, trust, and fallback strategies; results should be cached, versioned, and tied to source timestamps.

20. Which sources would you add in production?
- **Basic:** VirusTotal, AbuseIPDB, OTX.
- **Intermediate:** GreyNoise, Shodan, WhoisXML, URLScan.io, PassiveTotal, PassiveDNS, Internal proxy/DNS/EDR logs.
- **Advanced:** Internal sources first: proxy logs, DNS, firewall, EDR, SIEM. External sources should drive hypothesis enrichment after internal telemetry reduces ambiguity.

### MITRE ATT&CK

21. What is MITRE ATT&CK?
- **Basic:** A knowledge base of attacker tactics and techniques.
- **Intermediate:** Tactics like Execution and Persistence map to techniques such as T1059.001 PowerShell; ThreatScope maps IOCs and rules to relevant techniques for coverage analysis.
- **Advanced:** ATT&CK gives analysts a shared vocabulary for detection gaps, threat hunting hypotheses, compliance matrices, and SOC reporting. Real tooling must normalize tactics across Enterprise, Mobile, and ICS matrices and handle overlapping technique applicability.

22. Why map IOCs to MITRE?
- **Basic:** To understand attacker behavior, not just indicators.
- **Intermediate:** Mapping reveals technique coverage gaps and supports hunting queries tied to lifecycle phases.
- **Advanced:** Coverage-aware SOC operations depend on technique/tactic mapping to prioritize detections, track adversary emulation progress, and report SOC maturity.

23. What are coverage gaps?
- **Basic:** Techniques that lack associated detections or indicators.
- **Intermediate:** ThreatScope counts IOCs and rules per technique and highlights low-coverage tactics.
- **Advanced:** Coverage analysis must distinguish between rules/rules coverage and tested/enforced coverage; static rule counts mislead. True coverage needs validation from detections, telemetry pipelines, and red/blue team confirmation.

### Sigma / YARA

24. What is Sigma?
- **Basic:** A rule format for describing log patterns.
- **Intermediate:** Sigma enables portable detection logic across SIEMs like Splunk, Elastic, and Sentinel.
- **Advanced:** SOC maturity depends on a governed Sigma lifecycle: authoring, conversion, review, coverage tracking, and validation against known logs.

25. What is YARA?
- **Basic:** A pattern-matching language for files.
- **Intermediate:** Used to classify malware samples based on byte patterns, strings, and metadata.
- **Advanced:** YARA rules need performance governance, false positive tracking, compilation management, and version control; they are also valuable in IoC hunting on file archives and endpoint artifacts.

26. How do you validate Sigma/YARA rules?
- **Basic:** Check required keywords like `title:` and `condition:`.
- **Intermediate:** Parse and lint rules, run converters, and handle validation errors in API responses.
- **Advanced:** Validation should include schema conformance, test datasets with expected matches, performance profiling, and promotion gating before prod environments consume rules.

### Docker

27. Why Docker Compose?
- **Basic:** One command to start PostgreSQL, Elasticsearch, backend, frontend, and Redis together.
- **Intermediate:** Ensures consistent local and demo environments, making recruitment demos, screenshots, and onboarding reproducible.
- **Advanced:** Compose is not production orchestration; for production workloads prefer Kubernetes/Helm, secrets backends, network segmentation, resource limits, logging drivers, and observability stack.

### Detection Engineering

28. What is detection engineering in your project?
- **Basic:** Writing Sigma rules for attacks.
- **Intermediate:** Creating detection logic, mapping it to MITRE techniques, and measuring coverage.
- **Advanced:** Detection engineering includes ingest normalization, field mapping per data source, S lie/drop tuning, rolling out changes with CI/CD for rules, analytics-driven false positive reduction, and threat-hunt hypotheses derived from coverage gaps.

29. How would you tune false positives?
- **Basic:** Add more conditions to the rule to ignore normal traffic.
- **Intermediate:** Use whitelists, exceptions, risk scoring thresholds, and correlation to suppress noisy alerts.
- **Advanced:** Build a feedback loop: SOC analysts promote/demote rules, correlate with asset criticality, implement adaptive thresholds using Bayesian or frequency-based scoring, and track alert fatigue metrics.

30. How do you measure SOC effectiveness?
- **Basic:** Count detections and time to respond.
- **Intermediate:** Measure coverage, mean time to detect, false positive rate, and rule effectiveness.
- **Advanced:** Combine coverage metrics with maturity scoring, teammate review cycles, threat hunt insights, and compliance posture across ATT&CK, NIST CSF, and organizational KPIs.

### SOC Operations

31. What is an alert lifecycle?
- **Basic:** Alert is created, analyst review, enrichment, decision, closure.
- **Intermediate:** Tracking state, owner, severity, investigation notes, related IOCs, and post-incident tagging.
- **Advanced:** Alert routing policies, SLA timers, SOAR integration hooks, PII minimization during sharing, structured closure categories, and RCA extraction into detection improvement.

32. How does IOC search help an analyst?
- **Basic:** Quickly look up suspicious indicators.
- **Intermediate:** Filter by type, risk, or keyword to support incident response pivots.
- **Advanced:** Investigators need correlated context: source trust, historical prevalence, timeline trends, technique mapping, alert linkage, and export-ready evidence packets for tickets and compliance.

### Threat Hunting

33. What is threat hunting based on MITRE?
- **Basic:** Searching for attacker behavior using ATT&CK tactics and techniques.
- **Intermediate:** Hypothesis-driven searches over telemetry using known techniques.
- **Advanced:** Hunting must validate detection coverage, iterate on fingerprinting, integrate TI pivots, document negative findings, and map discovered activity to ATT&CK for executive reporting.

34. How would you design hunting queries in this project?
- **Basic:** Use IOC search and correlation endpoints.
- **Intermediate:** Combine IOC/alert filters with risk thresholds and technique filters.
- **Advanced:** Provide time windows, asset context correlation, behavior joins, saved hunt templates, query export, and machine-assisted hypothesis ranking by coverage gaps and observed activity.

### Security

35. How do you prevent secret leakage?
- **Basic:** Use `.env` files and don’t commit secrets.
- **Intermediate:** GitHub secret scanning, CI checks for `.env` and strong defaults.
- **Advanced:** Adopt vault-managed secrets, short-lived credentials, rotated keys, secret scanning pre-commit hooks, and least-privileged service identity for each component.

36. How do you limit plugin/rule abuse?
- **Basic:** Validate rules before saving.
- **Intermediate:** Restrict execution context, sandbox, and run static checks.
- **Advanced:** Use function whitelisting, resource budgets, rate-limiting conversions, and audit all rule creation/updates to prevent persistence abuse or deployment of malicious detections.

37. What are least privilege boundaries in ThreatScope?
- **Basic:** Read-only viewer access is different from analyst and admin access.
- **Intermediate:** Scoping ensures analysts cannot modify rules or users, while admins can.
- **Advanced:** Expand with attribute-based rules, approval-based promotions for detection content, separation of duties between ingestion and detection oversight, and network microsegmentation.

38. How do you secure ingest endpoints?
- **Basic:** Require authenticated requests and validate payloads.
- **Intermediate:** Rate limiting, schema validation, normalization, and partial rejection without service interruption.
- **Advanced:** Introduce WAF rules, request provenance checks, anomaly-based intake filtering for poisoning attacks, and source-based trust levels that gate persistence behavior.

### DevOps / CI

39. How does CI help a security project?
- **Basic:** Automatic tests and checks.
- **Intermediate:** Faster feedback on broken builds and quick identification of security fails.
- **Advanced:** Enforce signed releases, dependency review, SBOM generation, container scanning in Trivy, policy-as-code, and gate merges on test coverage/suspicious pattern density.

40. What is Infrastructure as Code value here?
- **Basic:** Keep infra layout in code.
- **Intermediate:** Docker Compose and repo scripts make setup reproducible.
- **Advanced:** IaC allows peer review of runtime topology, reduces configuration drift, supports compliance evidence, and enables self-service iterations during SOC assessments.

### Others

41. How do you document a security project?
- **Basic:** README, docs folders, diagrams.
- **Intermediate:** Write Mermaid diagrams, API contracts, deployment steps, and example payloads.
- **Advanced:** Treat docs as part of security evidence: redaction rules, audience-specific variants for analysts vs execs, change control, and audit-friendly JSON/OpenAPI artifacts.

42. What should a recruiter see first in this repo?
- **Basic:** README with project title, description, and features.
- **Intermediate:** Badges, architecture diagram, installation steps, demo screenshot, and active CI indicators.
- **Advanced:** Strong README TL;DR showing SOC-relevant impact, clear threat domain, real working endpoints, security hygiene, tests, and contribution/support signals.

43. Why project documentation is important for interviews?
- **Basic:** To show you understand the product and can explain it.
- **Intermediate:** It shows communication, structure, and awareness of users/analysts/security managers.
- **Advanced:** Technical documentation demonstrates you operate in enterprise mode: banking on repeatability, onboarding reuse, audit readiness, and customer/colleague trust.

44. How would you demo this project in an interview?
- **Basic:** Run backend and show IOC ingest/search endpoints.
- **Intermediate:** Walk through ingest, enrichment, search, risk scoring, and reporting in a scripted flow using curl or Swagger UI.
- **Advanced:** Tell a threat story: ingest actor IOCs, map to ATT&CK, score risks, and produce the report; explain analyst benefits, coverage gaps found, and how this mirrors commercial CTI platforms.

45. What improvements would you make for enterprise use?
- **Basic:** Add authentication, logging, and more sources.
- **Intermediate:** Add multi-tenant isolation, SSO, role schemas, audit trails, and SLA-aware ingestion backoff.
- **Advanced:** Harden with Zero Trust principles, egress filtering, runtime secrets rotation, dataclass-aware storage partitioning, privacy-by-design for PII indicators, SLO monitoring, and integrated IR/SOAR handoff.

46. How do you define threat actor attribution?
- **Basic:** Linking indicators to known actor groups.
- **Intermediate:** Persistent IDs, metadata fields, IOC linkage, and references.
- **Advanced:** Attribution must express confidence, avoid over-attribution, maintain source attribution chains, and align with vendor intel sharing standards like STIX `threat-actor` with observed relationships.

47. What metrics would you track?
- **Basic:** Indicator count, alerts, search rate.
- **Intermediate:** Ingestion latency, enrichment coverage, correlation rate, error rate by source, rule validation pass rate, scoring distribution.
- **Advanced:** Time-to-enrich, ATT&CK coverage delta, false-positive ratio, analyst dwell time, rule churn, ingestion backlog age, and SLA compliance.

48. Explain caching/queuing choice.
- **Basic:** Redis for speed; queues for decoupling.
- **Intermediate:** Redis stores rate-limit state and session cache; queues buffer ingestion from slower external APIs.
- **Advanced:** Production adds priority queues per source, dead-letter handling, distributed cache invalidation on schema changes, and worker autoscaling via queue depth.

49. What testing types matter here?
- **Basic:** Unit tests for endpoints and services.
- **Intermediate:** Integration tests with test DB, schema fixtures, ingest pipelines, and risk scoring accuracy checks.
- **Advanced:** Contract tests for TI feeds, security tests against auth/RBAC boundaries, chaos testing for queue/db failures, regression tests for rules, and red-team honing exercises logged as tests.

50. Why not connect live TI sources in portfolio code?
- **Basic:** It can be expensive or unsafe.
- **Intermediate:** Demo endpoints provide reproducible behavior for interviews without relying on third-party availability or billing.
- **Advanced:** Production requires API key management, quota handling, egress controls, data-flow privacy review, and consent for sample data. Portfolio code should behave deterministically while showing correct separation for future integration.

---

## 20 HR Questions

51. Why did you build ThreatScope?
- **Basic:** To practice backend, database, and security concepts together.
- **Intermediate:** To build end-to-end SOC-relevant tooling that mirrors real CTI platforms.
- **Advanced:** To demonstrate capability across ingestion, correlation, scoring, detection, MITRE alignment, and interview-speaking documentation that matches enterprise roles.

52. What challenges did you face?
- **Basic:** Organizing modules and setting up the project.
- **Intermediate:** Choosing data model trade-offs and API layer isolation.
- **Advanced:** Balancing MVP scope versus portfolio depth, managing async/DB complexity, and writing reusable modules usable in real interviews through structured docs and demo scripts.

53. How did you prioritize features?
- **Basic:** Core endpoints first, then docs.
- **Intermediate:** IOC search and enrichment were prioritized for immediate SOC utility; MITRE and scoring layered on top.
- **Advanced:** Priorities aligned with interview audiences: working code, credible architecture docs, tests, and security posture over aspirational future branches.

54. How did you scale the platform?
- **Basic:** Modularized backend service layer.
- **Intermediate:** Queueable ingestion, cached searches, separated auth, and CI-secured build flow.
- **Advanced:** Designed for extension by isolating external integrations behind services, database-layer partitioning readiness, and logger-structured telemetry for future scaling decisions.

55. What did you learn?
- **Basic:** API design and database relationships.
- **Intermediate:** SOC workflows, IOC enrichment complexity, and MITRE mapping needs.
- **Advanced:** Portfolio professionalization: documentation quality, test discipline, CI policy, interview storytelling, and realistic acknowledgment of limitations vs enterprise gaps.

56. How did you collaborate on this?
- **Basic:** This is a solo project, but I planned a realistic team structure.
- **Intermediate:** I used standard conventions for docs, CI, commit messages, and contribution guidelines to make it appear production-grade.
- **Advanced:** Future contributions can use Branch/PR standards, peer review simulation, security review processes, and shared ownership rules.

57. What is the most SOC-relevant part?
- **Basic:** IOC search and alerts.
- **Intermediate:** Correlation and risk scoring.
- **Advanced:** MITRE coverage, evidence curation, and analyst investigation workflow; without these, security tooling is just a CRUD app.

58. Could this be used in production?
- **Basic:** Not yet, as-is.
- **Intermediate:** It can demonstrate core workflows, but lacks e2e hardening, secret handling, logging, and monitoring.
- **Advanced:** With authentication hardening, SOAR tie-ins, multi-tenant isolation, hardened container hardening, and SOC policy tuning, the platform pattern is directly translatable to an internal CTI service; currently it is portfolio-grade and POC-ready.

59. How would you present this to a SOC Manager?
- **Basic:** Show how to ingest and search indicators.
- **Intermediate:** Show scoring, correlation, and reports versus increasing alert fatigue.
- **Advanced:** Present baseline context: enables junior analysts to investigate faster, reduces time-to-context, provides coverage reporting to justify staffing and tooling, and improves evidence-backed reporting.

60. How would you present this to a Threat Intel Lead?
- **Basic:** Collect indicators from multiple sources.
- **Intermediate:** Normalize, dedup, enrich, attribute, and export reports.
- **Advanced:** Show STIX-compatible data model, source provenance, confidence scoring, and MITRE mapping that accelerate TTP-based distilling and cross-sharing with teammates and stakeholders.

61. How do you handle sensitive data in the app?
- **Basic:** Avoid committing secrets and raw incidents.
- **Intermediate:** Designed with environment-based secrets, PII minimization, and sample datasets separated from configs.
- **Advanced:** Would add redaction policies, data-classification TLS-in-transit, storage encryption, audit logging, and SOC2-style evidence controls.

62. How do you keep the project up-to-date?
- **Basic:** Update dependencies and docs.
- **Intermediate:** Track model, tool, and API freshness for TI sources and Python dependencies.
- **Advanced:** Use live dependency review, version-pinned manifests, signed tags, automated update PRs with vulnerability review, and change documentation in CHANGELOG.

63. What’s next for the project?
- **Basic:** Add more features and fix bugs.
- **Intermediate:** Build a frontend dashboard, async queue workers, enrichment API integrations, and reporting PDF exports.
- **Advanced:** Expand detection and coverage analytics, integrate with mock-SIEM endpoints, improve RBAC with SSO, and produce a paper/interview kit from the structured docs authored here.

64. Tell me about your commit message style.
- **Basic:** Short working descriptions.
- **Intermediate:** Conventional Commits with type/scope, reflecting team conventions.
- **Advanced:** Commit discipline demonstrates change traceability, automation readiness, and compliance evidence—qualities enterprise reviewers expect and CI systems exploit.

65. Why did you add tests?
- **Basic:** To prove endpoints work.
- **Intermediate:** To prevent regressions and support future changes confidently.
- **Advanced:** Tests act as executable documentation, stabilize refactoring, support secure coding policies, and improve hiring signal from static review alone.

66. How does auth relate to SOC tooling?
- **Basic:** Controls who can access data.
- **Intermediate:** Different roles need different permissions like read-only vs admin.
- **Advanced:** Least privilege, separation of duties, and audit trails are required to prevent insider risk and misuse during incident response.

67. What is RBAC?
- **Basic:** Roles define allowed actions.
- **Intermediate:** `viewer`, `analyst`, `admin` have scopes controlling endpoint access.
- **Advanced:** RBAC must reflect organizational hierarchy, job-function boundaries, and require separation between TI pipeline writers and detection rule approvers in mature SOCs.

68. How do you explain your recent commits to a non-technical interviewer?
- **Basic:** Added search, rules, reports, and login.
- **Intermediate:** Added analyst-friendly features: IOC investigation, enrichment, correlation, and addition of attacker behavior mapping.
- **Advanced:** Articulated security operations improvement: less time gathering context, faster triage, searchable knowledge base, and measurable detection coverage.

69. What would you improve first in a real team?
- **Basic:** Add real external APIs.
- **Intermediate:** Build UI, integrations, and enrichment adaptability.
- **Advanced:** Prioritize auth hardening, defendable change control, incident response runbooks tied to the tool, and threat-hunt experiment logging so the platform becomes repeatable practice rather than a demo.

70. What standards/regulations are relevant here?
- **Basic:** General security awareness.
- **Intermediate:** Awareness of logging access and retention requirements relevant to SOC workflows.
- **Advanced:** Alignment with NIST CSF/SP 800-61, ISO 27001, SOC2, and regulatory view of TI-sharing consent; platform design should be able to produce evidence outputs.

---

## Interview Storytelling Cheat Sheet

Use this concise narrative when asked walk-through questions.

1. **Problem:** SOC analysts need a centralized place to ingest indicators, assess risk, find attacker techniques, and investigate quickly.
2. **Solution:** ThreatScope provides a FastAPI backend with ingestion, IOC management, correlation, scoring, MITRE mapping, Sigma/YARA rule management, reporting, and RBAC.
3. **Implementation highlights:** Deterministic UUID-based IOC dedup, source-provenance tracking, lightweight scoring heuristics, separation between policy (score weights) and data (IOC rows), and modular routers ready for rest expansion.
4. **Validation:** Automated tests cover happy paths; architecture docs show reasoning and trade-offs.
5. **Next:** Add frontend dashboard, real enrichment integrations, richer correlation heuristics, and automated experimentation on detection effectiveness.

---

## Sample Answer Format Cheat Sheet

- **Basic:** One paragraph, non-jargon, speaks to intent and value.
- **Intermediate:** Adds implementation specifics and SOC relevance.
- **Advanced:** Adds scaling, trust boundaries, policy, governance, and measurement.

Use the questions above to practice switching between those layers depending on your interviewer’s seniority.
