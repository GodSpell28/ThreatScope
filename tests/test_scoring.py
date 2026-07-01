import os
import sys
import pytest

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(BACKEND)

from app.models.ioc import IOC
from app.services.scoring import calculate_ioc_risk, calculate_batch_risk


def test_scoring_basic():
    ioc = IOC(id="1", type="domain", value="malicious.example", confidence=0.8, sources=[])
    result = calculate_ioc_risk(ioc)
    assert "risk_score" in result
    assert 0 <= result["risk_score"] <= 100


def test_scoring_with_sources():
    ioc = IOC(id="2", type="ipv4", value="198.51.100.10", confidence=0.9, sources=[])
    for _ in range(5):
        ioc.sources.append(type("src", (), {"source_name": "vt"})())
    result = calculate_ioc_risk(ioc)
    assert result["risk_score"] >= result["source_component"]
