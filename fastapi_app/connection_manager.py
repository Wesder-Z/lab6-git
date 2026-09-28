"""Управление активными WebSocket-соединениями."""

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Хранит подключения и рассылает сообщения участникам чата."""

    def __init__(self) -> None:
        self._connections: list[WebSocket] = []

    @property
    def connection_count(self) -> int:
        """Количество активных подключений."""
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        """Принимает WebSocket-соединение и сохраняет его."""
        await websocket.accept()
        self._connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Удаляет соединение, если оно ещё зарегистрировано."""
        if websocket in self._connections:
            self._connections.remove(websocket)

    async def broadcast(self, message: dict[str, str]) -> None:
        """Отправляет JSON-сообщение всем активным клиентам.

        Args:
            message: Сериализованное событие чата.
        """
        disconnected: list[WebSocket] = []
        for connection in self._connections.copy():
            try:
                await connection.send_json(message)
            except (RuntimeError, WebSocketDisconnect):
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)
