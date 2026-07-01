from typing import List, Dict, Any
from app.models.ioc import IOC, IOCSource
from app.models.technique import Technique
from collections import defaultdict


def generate_ioc_report(iocs: List[IOC]) -> Dict[str, Any]:
    type_distribution: Dict[str, int] = defaultdict(int)
    source_frequency: Dict[str, int] = defaultdict(int)
    avg_risk = 0.0
    for ioc in iocs:
        type_distribution[ioc.type or "unknown"] += 1
        avg_risk += float(ioc.risk_score or 0.0)
        for source in ioc.sources:
            source_frequency[source.source_name] += 1
    avg_risk = round(avg_risk / max(len(iocs), 1), 4) if iocs else 0.0
    return {
        "ioc_count": len(iocs),
        "high_risk_count": sum(1 for i in iocs if (i.risk_score or 0.0) >= 70),
        "medium_risk_count": sum(1 for i in iocs if 40 <= (i.risk_score or 0.0) < 70),
        "low_risk_count": sum(1 for i in iocs if (i.risk_score or 0.0) < 40),
        "avg_risk_score": avg_risk,
        "type_distribution": dict(type_distribution),
        "source_frequency": dict(source_frequency),
    }


def generate_threat_report(iocs: List[IOC], techniques: List[Technique]) -> Dict[str, Any]:
    technique_map = {t.id: t for t in techniques}
    coverage: Dict[str, int] = defaultdict(int)
    for ioc in iocs:
        for technique in getattr(ioc, "techniques", []):
            coverage[technique.id] += 1
    top_techniques = sorted(
        [{"technique_id": k, "tactic": technique_map[k].tactic, "ioc_count": v} for k, v in coverage.items()],
        key=lambda x: x["ioc_count"],
        reverse=True,
    )[:10]
    return {
        "technique_coverage_count": len(coverage),
        "top_techniques": top_techniques,
    }
