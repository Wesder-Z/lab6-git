# Лабораторная работа № 6

**Борисов Анатолий Олегович, группа 221141, вариант 5, лабораторная № 6**

Дисциплина: «Методы и технологии программирования».

## Цель работы

Создать веб-приложения на Flask и FastAPI, освоить HTML-шаблоны, JSON API,
Pydantic-схемы и двусторонний обмен сообщениями через WebSocket.

## Задания варианта

| Сложность | № | Задание | Реализация |
|---|---:|---|---|
| Средняя | 5 | Страница с Bootstrap | Адаптивная Jinja-страница на Bootstrap 5.3.8 |
| Средняя | 7 | FastAPI endpoint возвращает JSON | `GET /api/info` возвращает сведения о сервисе и студенте |
| Средняя | 1 | Flask-приложение «Hello World» | `GET /` возвращает текст «Привет, Flask!» |
| Повышенная | 6 | Чат на WebSocket FastAPI | Локальный чат рассылает сообщения всем подключённым клиентам |
| Повышенная | 8 | Использование Pydantic-схем | Схемы проверяют запросы, ответы и сообщения чата |

## Структура проекта

- `flask_app.py` содержит фабрику Flask-приложения;
- `templates/bootstrap.html` содержит адаптивную Bootstrap-страницу;
- `fastapi_app/main.py` содержит REST и WebSocket endpoints;
- `fastapi_app/schemas.py` содержит Pydantic-схемы;
- `fastapi_app/connection_manager.py` управляет подключениями чата;
- `fastapi_app/static/chat.html` содержит браузерный клиент чата;
- `tests/` содержит тесты Flask, REST API, схем и WebSocket;
- `.github/workflows/python-check.yml` запускает проверки на GitHub Actions.

## Установка

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Linux и macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Запуск Flask

```bash
python -m flask --app flask_app run
```

- приветствие: `http://127.0.0.1:5000/`;
- Bootstrap-страница: `http://127.0.0.1:5000/bootstrap`.

## Запуск FastAPI

```bash
python -m uvicorn fastapi_app.main:app --reload
```

- JSON endpoint: `http://127.0.0.1:8000/api/info`;
- локальный чат: `http://127.0.0.1:8000/chat`;
- Swagger UI: `http://127.0.0.1:8000/docs`.

Чат хранит активные подключения в памяти одного процесса. Сообщения не
сохраняются после остановки сервера. На странице используется `textContent`,
поэтому полученный текст не интерпретируется браузером как HTML-код. Кнопка
отправки доступна только после установки WebSocket-соединения.

## REST API и схемы

| Метод | Адрес | Назначение |
|---|---|---|
| `GET` | `/api/info` | Получить JSON с информацией о сервисе |
| `POST` | `/api/messages` | Проверить сообщение Pydantic-схемой |
| `GET` | `/chat` | Открыть страницу локального чата |
| `WebSocket` | `/ws/chat` | Обмен сообщениями между клиентами |

`ChatMessage` ограничивает длину имени и сообщения, удаляет внешние пробелы и
отклоняет строки, состоящие только из пробелов. FastAPI автоматически формирует
описание этих схем в OpenAPI.

## Проверка

```bash
python -m pip install -r requirements-dev.txt
python -m compileall -q .
python -m flake8 .
python -m pytest -v
```

Тесты проверяют оба маршрута Flask, JSON-ответы, ошибки валидации, наличие схем
в OpenAPI, страницу чата, обработку неверного сообщения и рассылку между двумя
WebSocket-клиентами. GitHub Actions повторяет эти проверки для ветки `main`,
тега `lab6` и pull request.
