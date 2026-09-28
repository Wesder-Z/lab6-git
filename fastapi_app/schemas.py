"""Pydantic-схемы REST API и WebSocket-чата."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ServiceInfo(BaseModel):
    """Информация о работающем API."""

    service: Literal["lab6-api"] = "lab6-api"
    status: Literal["ok"] = "ok"
    student: str
    group: int
    variant: int


class ChatMessage(BaseModel):
    """Сообщение, полученное от участника чата."""

    author: str = Field(min_length=2, max_length=30)
    text: str = Field(min_length=1, max_length=300)

    @field_validator("author", "text")
    @classmethod
    def strip_and_validate_text(cls, value: str) -> str:
        """Удаляет внешние пробелы и запрещает строки из пробелов."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Значение не должно состоять только из пробелов")
        return cleaned


class ChatEvent(ChatMessage):
    """Сообщение, отправляемое всем подключённым клиентам."""

    type: Literal["message"] = "message"


class SystemEvent(BaseModel):
    """Служебное сообщение WebSocket-чата."""

    type: Literal["system", "error"]
    detail: str
