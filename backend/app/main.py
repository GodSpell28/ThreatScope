from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import iocs, health

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


@app.get("/")
async def root():
    return {"service": "threatscope", "status": "ok"}
