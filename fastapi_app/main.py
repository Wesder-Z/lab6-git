"""FastAPI-приложение с JSON API и WebSocket-чатом."""

from json import JSONDecodeError
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import ValidationError

from fastapi_app.connection_manager import ConnectionManager
from fastapi_app.schemas import ChatEvent, ChatMessage, ServiceInfo, SystemEvent


CHAT_PAGE = Path(__file__).parent / "static" / "chat.html"

app = FastAPI(
    title="Лабораторная работа № 6",
    description="JSON API и локальный WebSocket-чат.",
    version="1.0.0",
)
manager = ConnectionManager()


@app.get("/api/info", response_model=ServiceInfo)
async def get_service_info() -> ServiceInfo:
    """Возвращает JSON с информацией о сервисе и авторе."""
    return ServiceInfo(
        student="Борисов Анатолий Олегович",
        group=221141,
        variant=5,
    )


@app.post("/api/messages", response_model=ChatEvent)
async def validate_message(message: ChatMessage) -> ChatEvent:
    """Проверяет сообщение Pydantic-схемой и формирует событие."""
    return ChatEvent(author=message.author, text=message.text)


@app.get("/chat", response_class=FileResponse)
async def get_chat_page() -> FileResponse:
    """Отдаёт браузерную страницу локального чата."""
    return FileResponse(CHAT_PAGE)


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket) -> None:
    """Получает проверенные сообщения и рассылает их всем клиентам."""
    await manager.connect(websocket)
    connected = SystemEvent(type="system", detail="Соединение установлено")
    await websocket.send_json(connected.model_dump())

    try:
        while True:
            try:
                payload = await websocket.receive_json()
                message = ChatMessage.model_validate(payload)
            except (JSONDecodeError, TypeError, ValidationError, ValueError):
                error = SystemEvent(
                    type="error",
                    detail="Укажите автора от 2 до 30 символов и сообщение",
                )
                await websocket.send_json(error.model_dump())
                continue

            event = ChatEvent(author=message.author, text=message.text)
            await manager.broadcast(event.model_dump())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
