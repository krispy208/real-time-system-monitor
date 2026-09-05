"""WebSocket client registry and broadcast helpers."""

import asyncio
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Track active dashboard WebSocket clients and push telemetry JSON to all of them.

    Broadcast is async because ``send_json`` performs network I/O. Clients that
    fail to receive a message are treated as stale and removed so one broken
    connection cannot block updates to the rest.
    """

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def active_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)
        logger.info("WebSocket client connected (%d active)", self.active_count)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)
        logger.info("WebSocket client disconnected (%d active)", self.active_count)

    async def broadcast(self, message: dict) -> None:
        async with self._lock:
            connections = list(self._connections)

        if not connections:
            return

        stale: list[WebSocket] = []
        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                stale.append(websocket)

        for websocket in stale:
            await self.disconnect(websocket)
