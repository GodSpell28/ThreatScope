from typing import List, Dict, Tuple
from collections import defaultdict
from app.models.ioc import IOC


def _build_value_index(iocs: List[IOC]) -> Dict[str, List[IOC]]:
    index: Dict[str, List[IOC]] = defaultdict(list)
    for ioc in iocs:
        index[ioc.value].append(ioc)
    return dict(index)


def correlate_iocs(iocs: List[IOC]) -> List[Tuple[str, str, float]]:
    index = _build_value_index(iocs)
    seen = set()
    results: List[Tuple[str, str, float]] = []
    for ioc in iocs:
        related = index.get(ioc.value, [])
        for other in related:
            if ioc is other:
                continue
            key = tuple(sorted([ioc.id, other.id]))
            if key in seen:
                continue
            seen.add(key)
            score = round((ioc.risk_score + other.risk_score) / 2, 4)
            results.append((ioc.id, other.id, score))
    return results
