import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.ws.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

router = APIRouter()


def _get_manager(websocket: WebSocket) -> ConnectionManager:
    return websocket.app.state.connection_manager


@router.websocket("/telemetry")
async def telemetry_stream(websocket: WebSocket) -> None:
    """Accept a client and hold the connection open for server-push telemetry."""
    manager = _get_manager(websocket)
    await manager.connect(websocket)

    try:
        while True:
            # Block here so FastAPI keeps the socket alive and detects disconnects.
            # Clients do not need to send messages; input is ignored.
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.debug("WebSocket client disconnected normally")
    finally:
        await manager.disconnect(websocket)
