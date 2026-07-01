import os
import sys
import pytest

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(BACKEND)

from app.services.correlation import correlate_iocs
from app.models.ioc import IOC


def test_correlation():
    iocs = [
        IOC(id="1", type="ipv4", value="198.51.100.10", risk_score=0.6),
        IOC(id="2", type="domain", value="malicious.example", risk_score=0.8),
        IOC(id="3", type="ipv4", value="198.51.100.10", risk_score=0.9),
    ]
    results = correlate_iocs(iocs)
    assert len(results) == 1
    assert results[0][2] == 0.75
