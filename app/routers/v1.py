from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.handlers import handle_login, handle_register
from app.schemas import AuthRequest, RegisterResponse, TokenResponse

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
    summary="Регистрация нового пользователя",
    responses={
        201: {"description": "Пользователь успешно создан"},
        409: {"description": "Пользователь с таким email уже существует"},
        422: {"description": "Ошибка валидации (неверный email или пароль < 6 символов)"},
    },
)
def register(payload: AuthRequest, db: Session = Depends(get_db)):
    """Создаёт нового пользователя. Email должен быть уникальным, пароль — минимум 6 символов."""
    return handle_register(payload, db)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Вход в систему",
    responses={
        200: {"description": "Успешный вход, возвращает JWT токен"},
        401: {"description": "Неверный email или пароль"},
        422: {"description": "Ошибка валидации"},
    },
)
def login(payload: AuthRequest, db: Session = Depends(get_db)):
    """Проверяет email и пароль, возвращает JWT `access_token`. Передавать в заголовке: `Authorization: Bearer <token>`."""
    return handle_login(payload, db)
