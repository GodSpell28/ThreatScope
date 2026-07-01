# ThreatScope Tests

## Run

```bash
pytest
```

## Notes
- Tests use `ASGITransport` with the FastAPI app in-memory.
- `conftest.py` sets safe defaults for environment variables used by auth, database, search, and caching.
- Seed scripts live under `backend/scripts/` and are independent of pytest.
- Some endpoints depend on external services like Elasticsearch; those tests are skipped when the service is unavailable if configured to do so by runner.
