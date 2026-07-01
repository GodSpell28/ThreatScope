# ThreatScope — 50 Technical Interview Questions

## Architecture
1. Describe ThreatScope end-to-end: ingest, normalize, correlate, score, alert, and report.
2. Why did you choose FastAPI for the backend?
3. How are the frontend and backend separated?
4. When would you split this into microservices?
5. Why store both PostgreSQL and Elasticsearch?

## APIs
6. What does `/api/v1/ingest/raw` accept?
7. How do you prevent duplicate IOCs?
8. What does `/api/v1/score` return?
9. How are versioned APIs handled?
10. When would you use gRPC over REST?

## Databases
11. Why normalize indicator values before hashing IDs?
12. How does the IOC-to-source relationship preserve provenance?
13. How would you partition `ioc_sources` at scale?
14. Why SQLAlchemy ORM vs raw SQL?
15. What Elasticsearch index mappings make sense for IOCs?

## Threat Intelligence
16. What is the difference between an IOC, TTP, and threat actor?
17. How do STIX bundles help interoperability?
18. Why is confidence scoring important?
19. How do you handle conflicting intelligence?
20. What does external enrichment add?

## IOC Enrichment
21. Which fields are most useful for enrichment?
22. How can passive DNS help triage?
23. What enrichment APIs fit this platform?
24. When is enrichment too costly to do inline?
25. How do caching and TTLs affect freshness?

## MITRE ATT&CK
26. Why map IOCs to techniques?
27. How does technique coverage detect blind spots?
28. What is the difference between tactic, technique, and sub-technique?
29. How would you automate MITRE mapping?
30. How do you report coverage gaps?

## Docker
31. Why Docker Compose rather than Kubernetes for MVP?
32. What is the order of service startup here?
33. How do you pass secrets in Docker safely?
34. What container security controls apply?
35. How do you debug an unhealthy backend container?

## Detection Engineering
36. Why keep Sigma and YARA alongside IOC data?
37. How would you convert a Sigma rule to a Splunk search?
38. What makes a rule high-signal vs noisy?
39. How do you measure detection coverage?
40. How does detection engineering relate to IOC feeds?

## SOC Operations
41. How would an analyst use ThreatScope during an alert?
42. What triage play does the dashboard enable?
43. How do risk scores change analyst prioritization?
44. What common IOC investigation pivots matter most?
45. How would you hand off findings to incident response?

## Threat Hunting
46. Which queries would a hunter run against this platform?
47. How do correlated IOCs suggest campaigns?
48. What hypotheses fit IOC correlation data?
49. How would you ingest custom intel for a threat hunt?
50. How do you validate a suspicious domain once it is in ThreatScope?
