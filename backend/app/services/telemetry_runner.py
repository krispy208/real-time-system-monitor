import asyncio
import logging

from app.monitoring.monitor import Monitor
from app.simulator import TelemetrySimulator
from app.state.store import StateStore
from app.ws.connection_manager import ConnectionManager
from app.ws.messages import build_telemetry_message

logger = logging.getLogger(__name__)

DEFAULT_INTERVAL_SECONDS = 1.0


async def run_telemetry_loop(
    store: StateStore,
    simulator: TelemetrySimulator,
    monitor: Monitor,
    connection_manager: ConnectionManager | None = None,
    interval_seconds: float = DEFAULT_INTERVAL_SECONDS,
) -> None:
    """Generate telemetry in the background and persist results to the state store."""
    logger.info("Telemetry background loop started")
    try:
        while True:
            for reading in simulator.next_readings():
                evaluation = monitor.evaluate(reading)
                alerts = monitor.latest_alerts
                store.record(evaluation, alerts)

                if connection_manager is not None:
                    message = build_telemetry_message(evaluation, alerts)
                    await connection_manager.broadcast(message)

            await asyncio.sleep(interval_seconds)
    except asyncio.CancelledError:
        logger.info("Telemetry background loop stopped")
        raise


def seed_initial_readings(
    store: StateStore,
    simulator: TelemetrySimulator,
    monitor: Monitor,
) -> None:
    """Populate the store before the API starts accepting requests."""
    for reading in simulator.next_readings():
        evaluation = monitor.evaluate(reading)
        store.record(evaluation, monitor.latest_alerts)
