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
        title="Auth API",
        version="1.0.0",
        description=(
            "## Авторизация для мобильного приложения на Kotlin\n\n"
            "Два одинаковых набора эндпоинтов — `/api/v1` и `/api/v2`.\n\n"
            "### Как пользоваться:\n"
            "1. **Зарегистрируйтесь** через `/register` — получите `id` и `email`\n"
            "2. **Войдите** через `/login` — получите `access_token`\n"
            "3. Передавайте токен в заголовке: `Authorization: Bearer <token>`\n\n"
            "### Тело запроса (для register и login одинаковое):\n"
            "```json\n"
            '{"email": "user@example.com", "password": "минимум 6 символов"}\n'
            "```"
        ),
        routes=app.routes,
        tags=[
            {
                "name": "v1",
                "description": "Версия 1 API — `/api/v1/register`, `/api/v1/login`",
            },
            {
                "name": "v2",
                "description": "Версия 2 API — `/api/v2/register`, `/api/v2/login`",
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
