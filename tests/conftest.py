import os
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(BACKEND))


def pytest_configure(config):
    os.environ.setdefault("DATABASE_URL", "sqlite:///./pytest.db")
    os.environ.setdefault("SECRET_KEY", "test-secret")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    os.environ.setdefault("RATE_LIMIT_PER_MINUTES", "120")
    os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")


@pytest.fixture(autouse=True)
def _reset_app_state(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./pytest.db")
    yield
