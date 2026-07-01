"""Create ThreatScope Elasticsearch index and optionally seed sample IOC documents."""

import argparse
import json

from app.elasticsearch import get_es
from app.services.search import ensure_index, index_ioc

SAMPLE_IOCS = [
    {"id": "es-1", "type": "ipv4", "value": "198.51.100.10", "risk_score": 0.6, "confidence": 0.8, "source_count": 2, "first_seen": "2026-06-01T00:00:00Z", "last_seen": "2026-06-25T00:00:00Z"},
    {"id": "es-2", "type": "domain", "value": "malicious.example", "risk_score": 0.8, "confidence": 0.9, "source_count": 3, "first_seen": "2026-06-01T00:00:00Z", "last_seen": "2026-06-25T00:00:00Z"},
    {"id": "es-3", "type": "url", "value": "https://evil.example/payload", "risk_score": 0.7, "confidence": 0.7, "source_count": 1, "first_seen": "2026-06-05T00:00:00Z", "last_seen": "2026-06-20T00:00:00Z"},
    {"id": "es-4", "type": "hash", "value": "44d88612fea8a8f36de82e1278abb02f", "risk_score": 0.9, "confidence": 0.95, "source_count": 4, "first_seen": "2026-06-02T00:00:00Z", "last_seen": "2026-06-24T00:00:00Z"},
]


def seed_index(reset: bool) -> dict[str, Any]:
    es = get_es()
    if reset:
        try:
            es.indices.delete(index="threatscope-iocs")
        except Exception:
            pass
    setup = ensure_index()
    added = 0
    skipped = 0
    for doc in SAMPLE_IOCS:
        try:
            index_ioc(doc)
            added += 1
        except Exception:
            skipped += 1
    return {"setup": setup, "added": added, "skipped": skipped}


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed ThreatScope Elasticsearch index")
    parser.add_argument("--reset", action="store_true", help="Delete and recreate the index before seeding")
    args = parser.parse_args()
    result = seed_index(args.reset)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
