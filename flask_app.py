"""Flask-приложение с приветствием и Bootstrap-страницей."""

from flask import Flask, Response, render_template


def create_app(testing: bool = False) -> Flask:
    """Создаёт и настраивает Flask-приложение.

    Args:
        testing: Включить тестовый режим Flask.

    Returns:
        Настроенное приложение.
    """
    app = Flask(__name__)
    app.config["TESTING"] = testing

    @app.get("/")
    def hello_world() -> Response:
        return Response("Привет, Flask!", content_type="text/plain; charset=utf-8")

    @app.get("/bootstrap")
    def bootstrap_page() -> str:
        return render_template("bootstrap.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
