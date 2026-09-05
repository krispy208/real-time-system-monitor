import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.routes import ws_telemetry
from app.monitoring.monitor import Monitor
from app.services.telemetry_runner import run_telemetry_loop, seed_initial_readings
from app.simulator import TelemetrySimulator
from app.state.store import StateStore
from app.ws.connection_manager import ConnectionManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    store = StateStore()
    simulator = TelemetrySimulator()
    monitor = Monitor()
    connection_manager = ConnectionManager()

    seed_initial_readings(store, simulator, monitor)

    app.state.store = store
    app.state.connection_manager = connection_manager
    task = asyncio.create_task(
        run_telemetry_loop(store, simulator, monitor, connection_manager)
    )

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(ws_telemetry.router, prefix="/ws", tags=["websocket"])
