"""Тесты REST API, Pydantic-схем и WebSocket-чата."""

from fastapi.testclient import TestClient

from fastapi_app.main import app, manager


client = TestClient(app)


def test_info_endpoint_returns_json() -> None:
    response = client.get("/api/info")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {
        "service": "lab6-api",
        "status": "ok",
        "student": "Борисов Анатолий Олегович",
        "group": 221141,
        "variant": 5,
    }


def test_pydantic_schema_normalizes_message() -> None:
    response = client.post(
        "/api/messages",
        json={"author": "  Анатолий  ", "text": "  Привет!  "},
    )

    assert response.status_code == 200
    assert response.json() == {
        "author": "Анатолий",
        "text": "Привет!",
        "type": "message",
    }


def test_pydantic_schema_rejects_short_author() -> None:
    response = client.post(
        "/api/messages",
        json={"author": "Я", "text": "Привет!"},
    )

    assert response.status_code == 422


def test_pydantic_schema_rejects_blank_message() -> None:
    response = client.post(
        "/api/messages",
        json={"author": "Анатолий", "text": "   "},
    )

    assert response.status_code == 422


def test_openapi_contains_pydantic_schemas() -> None:
    response = client.get("/openapi.json")
    schemas = response.json()["components"]["schemas"]

    assert response.status_code == 200
    assert "ChatMessage" in schemas
    assert "ChatEvent" in schemas
    assert "ServiceInfo" in schemas


def test_chat_page_contains_websocket_client() -> None:
    response = client.get("/chat")

    assert response.status_code == 200
    assert "new WebSocket" in response.text
    assert "textContent" in response.text
    assert "/ws/chat" in response.text


def test_websocket_sends_validated_message() -> None:
    with client.websocket_connect("/ws/chat") as websocket:
        assert websocket.receive_json() == {
            "type": "system",
            "detail": "Соединение установлено",
        }
        websocket.send_json({"author": "Анатолий", "text": "Привет!"})

        assert websocket.receive_json() == {
            "author": "Анатолий",
            "text": "Привет!",
            "type": "message",
        }


def test_websocket_reports_validation_error() -> None:
    with client.websocket_connect("/ws/chat") as websocket:
        websocket.receive_json()
        websocket.send_json({"author": "Я", "text": ""})

        assert websocket.receive_json() == {
            "type": "error",
            "detail": "Укажите автора от 2 до 30 символов и сообщение",
        }


def test_websocket_broadcasts_to_two_clients() -> None:
    with client.websocket_connect("/ws/chat") as first:
        first.receive_json()
        with client.websocket_connect("/ws/chat") as second:
            second.receive_json()
            first.send_json({"author": "Анатолий", "text": "Всем привет!"})

            expected = {
                "author": "Анатолий",
                "text": "Всем привет!",
                "type": "message",
            }
            assert first.receive_json() == expected
            assert second.receive_json() == expected

    assert manager.connection_count == 0
