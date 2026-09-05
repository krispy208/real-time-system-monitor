from fastapi import APIRouter

from app.api.routes import alerts, health, systems, telemetry

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(systems.router)
api_router.include_router(telemetry.router)
api_router.include_router(alerts.router)
