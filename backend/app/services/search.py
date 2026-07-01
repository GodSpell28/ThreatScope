from typing import Any
from app.elasticsearch import get_es

INDEX_NAME = "threatscope-iocs"


def ensure_index() -> dict[str, Any]:
    es = get_es()
    if es.indices.exists(index=INDEX_NAME):
        return {"status": "exists", "index": INDEX_NAME}
    mappings = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "type": {"type": "keyword"},
                "value": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "risk_score": {"type": "float"},
                "confidence": {"type": "float"},
                "source_count": {"type": "integer"},
                "first_seen": {"type": "date"},
                "last_seen": {"type": "date"},
            }
        }
    }
    es.indices.create(index=INDEX_NAME, body=mappings)
    return {"status": "created", "index": INDEX_NAME}


def index_ioc(doc: dict[str, Any]) -> dict[str, Any]:
    es = get_es()
    es.index(index=INDEX_NAME, id=doc.get("id"), document=doc)
    return {"status": "indexed", "id": doc.get("id")}


def search_iocs(query: str, size: int = 50) -> dict[str, Any]:
    es = get_es()
    body = {
        "size": size,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["value", "type"],
                "fuzziness": "AUTO",
            }
        },
        "sort": [{"risk_score": {"order": "desc"}}],
    }
    resp = es.search(index=INDEX_NAME, body=body)
    hits = []
    for hit in resp.get("hits", {}).get("hits", []):
        src = hit.get("_source", {})
        src["_score"] = hit.get("_score")
        hits.append(src)
    return {"query": query, "count": len(hits), "results": hits}
