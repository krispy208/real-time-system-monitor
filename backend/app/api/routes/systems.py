from fastapi import APIRouter, HTTPException, Request

from app.api.schemas.mappers import to_system_detail, to_system_summary
from app.api.schemas.responses import SystemDetail, SystemSummary

router = APIRouter(prefix="/systems", tags=["systems"])


def _get_store(request: Request):
    return request.app.state.store


@router.get("", response_model=list[SystemSummary])
def list_systems(request: Request) -> list[SystemSummary]:
    store = _get_store(request)
    summaries: list[SystemSummary] = []

    for _system_id, state in store.get_all_system_states():
        if state.latest_evaluation is None:
            continue
        summaries.append(to_system_summary(state.latest_evaluation))

    return summaries


@router.get("/{system_id}", response_model=SystemDetail)
def get_system(system_id: str, request: Request) -> SystemDetail:
    store = _get_store(request)

    if not store.is_known_system(system_id):
        raise HTTPException(status_code=404, detail=f"Unknown system: {system_id}")

    state = store.get_system_state(system_id)
    if state is None or state.latest_evaluation is None:
        raise HTTPException(status_code=404, detail=f"Unknown system: {system_id}")

    return to_system_detail(state.latest_evaluation)
