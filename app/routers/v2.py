from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.handlers import (
    handle_get_challenge_states,
    handle_get_profile,
    handle_login,
    handle_register,
    handle_update_challenge_state,
    handle_update_profile,
)
from app.models import User
from app.schemas import (
    AuthRequest,
    ChallengeStateBulkResponse,
    ChallengeStateResponse,
    ChallengeStateUpdateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
    RegisterResponse,
    TokenResponse,
)

router = APIRouter(prefix="/api/v2", tags=["v2"])


# ─── Auth ─────────────────────────────────────────────────────────────────────

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
    """Создаёт нового пользователя и пустой профиль. Email уникален, пароль ≥ 6 символов."""
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


# ─── Profile ──────────────────────────────────────────────────────────────────

@router.get(
    "/profile",
    response_model=ProfileResponse,
    summary="Получить профиль",
    responses={
        200: {"description": "Профиль пользователя"},
        401: {"description": "Не авторизован"},
    },
)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Возвращает профиль авторизованного пользователя: email, очки, стрик, уровень."""
    return handle_get_profile(current_user, db)


@router.patch(
    "/profile",
    response_model=ProfileResponse,
    summary="Обновить профиль",
    responses={
        200: {"description": "Обновлённый профиль"},
        401: {"description": "Не авторизован"},
    },
)
def update_profile(
    payload: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Частичное обновление профиля — передавай только изменившиеся поля."""
    return handle_update_profile(current_user, payload, db)


# ─── Challenges ───────────────────────────────────────────────────────────────

@router.get(
    "/challenges",
    response_model=ChallengeStateBulkResponse,
    summary="Получить статусы всех заданий",
    responses={
        200: {"description": "Список статусов заданий пользователя"},
        401: {"description": "Не авторизован"},
    },
)
def get_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Возвращает сохранённые статусы заданий. Задания без записи считаются 'open'."""
    return handle_get_challenge_states(current_user, db)


@router.put(
    "/challenges/{challenge_id}",
    response_model=ChallengeStateResponse,
    summary="Обновить статус задания",
    responses={
        200: {"description": "Обновлённый статус задания"},
        401: {"description": "Не авторизован"},
        422: {"description": "Неверный статус или challenge_id"},
    },
)
def update_challenge(
    challenge_id: int,
    payload: ChallengeStateUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Устанавливает статус задания (open/active/checking/done/skipped) и опционально photo_url."""
    return handle_update_challenge_state(current_user, challenge_id, payload, db)
