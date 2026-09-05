from fastapi import APIRouter, Query, Request

from app.api.schemas.mappers import to_alert_response
from app.api.schemas.responses import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


def _get_repository(request: Request):
    return request.app.state.repository


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    request: Request,
    limit: int = Query(default=100, ge=1, le=1000),
    system_id: str | None = Query(default=None),
    severity: str | None = Query(default=None),
) -> list[AlertResponse]:
    repository = _get_repository(request)
    alerts = repository.get_alerts(
        limit=limit,
        system_id=system_id,
        severity=severity,
    )
    return [to_alert_response(alert) for alert in alerts]
