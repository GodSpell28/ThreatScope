from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import iocs, health, ingest, enrich, correlation, scoring, mitre, reports, rules
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ThreatScope API",
    description="Cyber Threat Intelligence & IOC Correlation Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(iocs.router, prefix="/api/v1/iocs", tags=["iocs"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["ingest"])
app.include_router(enrich.router, prefix="/api/v1/enrich", tags=["enrich"])
app.include_router(correlation.router, prefix="/api/v1/correlation", tags=["correlation"])
app.include_router(scoring.router, prefix="/api/v1/score", tags=["score"])
app.include_router(mitre.router, prefix="/api/v1/mitre", tags=["mitre"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(rules.router, prefix="/api/v1/rules", tags=["rules"])


@app.get("/")
async def root():
    return {"service": "threatscope", "status": "ok"}
