"""Тесты Flask-приложения."""

from flask.testing import FlaskClient

from flask_app import create_app


def make_client() -> FlaskClient:
    """Создаёт изолированный тестовый клиент Flask."""
    return create_app(testing=True).test_client()


def test_hello_world_route() -> None:
    response = make_client().get("/")

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.get_data(as_text=True) == "Привет, Flask!"


def test_bootstrap_page_uses_current_cdn() -> None:
    response = make_client().get("/bootstrap")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "bootstrap@5.3.8" in page
    assert 'name="viewport"' in page
    assert "Веб-программирование на Python" in page


def test_unknown_flask_route_returns_404() -> None:
    response = make_client().get("/missing")

    assert response.status_code == 404
