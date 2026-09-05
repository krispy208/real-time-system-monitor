import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.ws.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

router = APIRouter()


def _get_manager(websocket: WebSocket) -> ConnectionManager:
    return websocket.app.state.connection_manager


@router.websocket("/telemetry")
async def telemetry_stream(websocket: WebSocket) -> None:
    manager = _get_manager(websocket)
    await manager.connect(websocket)

    try:
        while True:
            # Keep the connection open; ignore any client messages.
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.debug("WebSocket client disconnected normally")
    finally:
        await manager.disconnect(websocket)
