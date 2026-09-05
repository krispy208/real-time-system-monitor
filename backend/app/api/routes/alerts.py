from fastapi import APIRouter, Request

from app.api.schemas.mappers import to_alert_response
from app.api.schemas.responses import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


def _get_store(request: Request):
    return request.app.state.store


@router.get("", response_model=list[AlertResponse])
def list_alerts(request: Request) -> list[AlertResponse]:
    store = _get_store(request)
    return [to_alert_response(alert) for alert in store.get_alerts()]
