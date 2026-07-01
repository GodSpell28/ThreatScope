import hashlib
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.ioc import IOC, IOCSource


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _derive_id(ioc_type: str, value: str) -> str:
    raw = f"{ioc_type}:{_normalize(value)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:64]


def _compute_risk_score(ioc: IOC) -> float:
    source_count = len(ioc.sources)
    confidence = float(ioc.confidence or 0.0)
    return round(min(1.0, max(0.0, 0.5 * confidence + 0.5 * min(source_count, 5) / 5)), 4)


def ingest_raw_iocs(db: Session, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    ingested = []
    duplicates = 0
    for item in items:
        ioc_type = str(item.get("type", "")).strip().lower()
        value = str(item.get("value", "")).strip()
        confidence = float(item.get("confidence", 0.0) or 0.0)
        if not ioc_type or not value:
            continue

        ioc_id = _derive_id(ioc_type, value)
        existing = db.get(IOC, ioc_id)
        if existing:
            existing.last_seen = datetime.utcnow()
            existing.confidence = max(existing.confidence, confidence)
            for src in item.get("sources", []):
                source_name = src.get("source_name")
                if not source_name:
                    continue
                match = next((s for s in existing.sources if s.source_name == source_name), None)
                if not match:
                    existing.sources.append(IOCSource(ioc_id=ioc_id, **src))
            existing.risk_score = _compute_risk_score(existing)
            db.add(existing)
            duplicates += 1
            continue

        ioc = IOC(
            id=ioc_id,
            type=ioc_type,
            value=_normalize(value),
            confidence=confidence,
            risk_score=0.0,
        )
        for src in item.get("sources", []):
            ioc.sources.append(IOCSource(ioc_id=ioc_id, **src))
        ioc.risk_score = _compute_risk_score(ioc)
        db.add(ioc)
        ingested.append(ioc)

    db.commit()
    return {
        "ingested": len(ingested),
        "duplicates": duplicates,
        "iocs": ingested,
    }


def ingest_stix_bundle(db: Session, bundle: Dict[str, Any]) -> Dict[str, Any]:
    items = []
    for obj in bundle.get("objects", []):
        obj_type = obj.get("type")
        if obj_type == "indicator":
            pattern = obj.get("pattern", "")
            # Very small parser only for demo purposes
            if pattern.lower().startswith("[ipv4-addr:value = '") and pattern.endswith("']"):
                value = pattern[len("[ipv4-addr:value = '"):-2]
                items.append({
                    "type": "ipv4",
                    "value": value,
                    "confidence": float(obj.get("confidence", 0.0) or 0.0),
                    "sources": [{"source_name": "stix", "external_id": obj.get("id"), "raw": pattern}],
                })
    if not items:
        return {"ingested": 0, "duplicates": 0, "iocs": []}
    return ingest_raw_iocs(db, items)
