from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="Real-Time System Monitor",
    description="Backend API for real-time system telemetry monitoring",
    version="0.1.0",
)

app.include_router(api_router)
