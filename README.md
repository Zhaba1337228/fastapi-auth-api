# fastapi-auth-api

Простое REST API на **FastAPI** + **PostgreSQL** с эндпоинтами регистрации и логина.  
Два одинаковых набора эндпоинтов — `/api/v1` и `/api/v2`.

---

## Стек

| Компонент | Версия |
|-----------|--------|
| Python    | 3.12   |
| FastAPI   | 0.115  |
| SQLAlchemy| 2.0    |
| PostgreSQL| 16     |
| JWT       | python-jose |
| Пароли    | bcrypt |

---

## Быстрый старт (Docker)

```bash
# 1. Клонировать
git clone https://github.com/<your-username>/fastapi-auth-api.git
cd fastapi-auth-api

# 2. Настроить переменные окружения
cp .env.example .env
# Поменяй POSTGRES_PASSWORD и JWT_SECRET в .env

# 3. Запустить
docker compose up -d --build

# API доступно на http://localhost:8000
# Swagger UI:  http://localhost:8000/docs
```

---

## Эндпоинты

### v1

| Метод | URL | Описание |
|-------|-----|----------|
| POST  | `/api/v1/register` | Регистрация |
| POST  | `/api/v1/login`    | Вход        |

### v2

| Метод | URL | Описание |
|-------|-----|----------|
| POST  | `/api/v2/register` | Регистрация |
| POST  | `/api/v2/login`    | Вход        |

---

## Тело запроса (одинаково для v1 и v2)

```json
{
  "email": "user@example.com",
  "password": "secretpass"
}
```

### Регистрация — ответ `201`

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Логин — ответ `200`

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

---

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `POSTGRES_USER` | `postgres` | Пользователь БД |
| `POSTGRES_PASSWORD` | `postgres` | Пароль БД |
| `POSTGRES_DB` | `appdb` | Имя базы |
| `JWT_SECRET` | `change-me-in-production` | Секрет для подписи токенов |
| `JWT_ALGORITHM` | `HS256` | Алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Время жизни токена (мин) |

---

## Остановить

```bash
docker compose down          # остановить контейнеры
docker compose down -v       # остановить + удалить volume с БД
```
