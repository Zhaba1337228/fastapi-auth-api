# fastapi-auth-api

REST API на FastAPI + PostgreSQL. Регистрация и логин, две версии эндпоинтов — `/api/v1` и `/api/v2`.

---

## Требования

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose (входит в Docker Desktop)
- Git

Больше ничего устанавливать не нужно — Python и PostgreSQL крутятся внутри контейнеров.

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Zhaba1337228/fastapi-auth-api.git
cd fastapi-auth-api
```

### 2. Создать файл с переменными окружения

```bash
cp .env.example .env
```

Открыть `.env` и поменять два значения:

```env
POSTGRES_PASSWORD=придумай_свой_пароль
JWT_SECRET=длинная_случайная_строка
```

> Остальные параметры можно оставить как есть.

### 3. Запустить

```bash
docker compose up -d --build
```

Первый запуск скачает образы и соберёт контейнер — займёт 1-2 минуты.

### 4. Открыть документацию (Swagger)

После запуска открой в браузере:

```
http://localhost:8000/docs
```

Там можно сразу тыкать эндпоинты — нажать на `/register` или `/login` → **Try it out** → вбить email и пароль → **Execute**. Без Postman и curl.

---

## Эндпоинты

Все эндпоинты принимают JSON с `email` и `password`.

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/v1/register` | Регистрация |
| POST | `/api/v1/login` | Вход |
| POST | `/api/v2/register` | Регистрация |
| POST | `/api/v2/login` | Вход |

### Тело запроса

```json
{
  "email": "user@example.com",
  "password": "минимум6символов"
}
```

### Ответ — регистрация `201`

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Ответ — логин `200`

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

Токен передавать в заголовке каждого запроса:

```
Authorization: Bearer eyJhbGci...
```

---

## Возможные ошибки

| Код | Причина |
|-----|---------|
| `409` | Пользователь с таким email уже зарегистрирован |
| `401` | Неверный email или пароль |
| `422` | Неверный формат email или пароль короче 6 символов |

---

## Остановить

```bash
docker compose down        # остановить, данные в БД сохранятся
docker compose down -v     # остановить и удалить БД полностью
```

---

## Переменные окружения (`.env`)

| Переменная | По умолчанию | Описание |
|---|---|---|
| `POSTGRES_USER` | `postgres` | Пользователь БД |
| `POSTGRES_PASSWORD` | `postgres` | Пароль БД — **обязательно поменяй** |
| `POSTGRES_DB` | `appdb` | Имя базы данных |
| `JWT_SECRET` | `change-me-in-production` | Секрет для JWT — **обязательно поменяй** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Время жизни токена в минутах (24 часа) |
