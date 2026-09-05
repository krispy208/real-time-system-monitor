import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.monitoring.monitor import Monitor
from app.services.telemetry_runner import run_telemetry_loop, seed_initial_readings
from app.simulator import TelemetrySimulator
from app.state.store import StateStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    store = StateStore()
    simulator = TelemetrySimulator()
    monitor = Monitor()

    seed_initial_readings(store, simulator, monitor)

    app.state.store = store
    task = asyncio.create_task(run_telemetry_loop(store, simulator, monitor))

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Real-Time System Monitor",
    description="Backend API for real-time system telemetry monitoring",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)
