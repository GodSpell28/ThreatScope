from typing import List, Dict, Any
from app.models.ioc import IOC


def calculate_ioc_risk(ioc: IOC) -> Dict[str, Any]:
    confidence = float(ioc.confidence or 0.0) * 40
    source_count = min(len(ioc.sources), 5) * 6
    risk_score = min(100, max(0, round(confidence + source_count)))
    recommendation = "high" if risk_score >= 70 else "medium" if risk_score >= 40 else "low"
    return {
        "confidence_component": round(confidence, 2),
        "source_component": source_count,
        "risk_score": risk_score,
        "recommendation": recommendation,
    }


def calculate_batch_risk(iocs: List[IOC]) -> List[Dict[str, Any]]:
    return [calculate_ioc_risk(ioc) for ioc in iocs]
