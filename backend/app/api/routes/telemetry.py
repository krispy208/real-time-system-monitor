from fastapi import APIRouter, HTTPException, Query, Request

from app.api.schemas.responses import TelemetryReadingResponse

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


def _get_store(request: Request):
    return request.app.state.store


def _get_repository(request: Request):
    return request.app.state.repository


@router.get("/{system_id}", response_model=list[TelemetryReadingResponse])
def get_telemetry_history(
    system_id: str,
    request: Request,
    limit: int = Query(default=100, ge=1, le=1000),
) -> list[TelemetryReadingResponse]:
    store = _get_store(request)

    if not store.is_known_system(system_id):
        raise HTTPException(status_code=404, detail=f"Unknown system: {system_id}")

    repository = _get_repository(request)
    history = repository.get_telemetry_history(system_id, limit)

    return [TelemetryReadingResponse(**row) for row in history]
