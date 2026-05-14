from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine
from app.routers import v1, v2

# Create tables on startup (for simplicity; use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(v1.router)
app.include_router(v2.router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title="Spark API",
        version="2.0.0",
        description=(
            "## Spark — API для мобильного приложения\n\n"
            "**v1** — только авторизация (legacy).\n\n"
            "**v2** — полный набор: авторизация + профиль + статусы заданий.\n\n"
            "---\n\n"
            "### Быстрый старт (v2)\n"
            "1. `POST /api/v2/register` — регистрация по email + password\n"
            "2. `POST /api/v2/login` — получить `access_token`\n"
            "3. Все остальные запросы: заголовок `Authorization: Bearer <token>`\n\n"
            "---\n\n"
            "### Профиль (`/api/v2/profile`)\n"
            "| Метод | Описание |\n"
            "|-------|----------|\n"
            "| `GET` | Получить профиль (email, courage, completed, skipped, streak, level, notifications) |\n"
            "| `PATCH` | Частично обновить профиль — передавай только изменившиеся поля |\n\n"
            "### Задания (`/api/v2/challenges`)\n"
            "| Метод | URL | Описание |\n"
            "|-------|-----|----------|\n"
            "| `GET` | `/challenges` | Все сохранённые статусы заданий пользователя |\n"
            "| `PUT` | `/challenges/{id}` | Установить статус задания: `open \\| active \\| checking \\| done \\| skipped` |\n"
        ),
        routes=app.routes,
        tags=[
            {
                "name": "v1",
                "description": "Версия 1 — только регистрация и вход.",
            },
            {
                "name": "v2",
                "description": (
                    "Версия 2 — авторизация, профиль, задания. "
                    "Все эндпоинты кроме `/register` и `/login` требуют `Authorization: Bearer <token>`."
                ),
            },
            {
                "name": "Health",
                "description": "Проверка работоспособности сервера",
            },
        ],
    )
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
