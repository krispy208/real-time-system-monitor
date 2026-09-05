from fastapi import APIRouter, HTTPException, Request

from app.api.schemas.responses import TelemetryReadingResponse

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


def _get_store(request: Request):
    return request.app.state.store


@router.get("/{system_id}", response_model=list[TelemetryReadingResponse])
def get_telemetry_history(system_id: str, request: Request) -> list[TelemetryReadingResponse]:
    store = _get_store(request)

    if not store.is_known_system(system_id):
        raise HTTPException(status_code=404, detail=f"Unknown system: {system_id}")

    history = store.get_telemetry_history(system_id)
    if history is None:
        raise HTTPException(status_code=404, detail=f"Unknown system: {system_id}")

    return [
        TelemetryReadingResponse(
            system_id=reading.system_id,
            timestamp=reading.timestamp,
            cpu_usage=reading.cpu_usage,
            memory_usage=reading.memory_usage,
            temperature=reading.temperature,
            latency=reading.latency,
        )
        for reading in history
    ]
