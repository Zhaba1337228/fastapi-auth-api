from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


# ─── Auth ────────────────────────────────────────────────────────────────────

class AuthRequest(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=6, examples=["secretpass"])

    model_config = {
        "json_schema_extra": {
            "examples": [{"email": "user@example.com", "password": "secretpass"}]
        }
    }

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT токен для авторизации")
    token_type: str = Field("bearer", description="Тип токена, всегда 'bearer'")

    model_config = {
        "json_schema_extra": {
            "examples": [{"access_token": "eyJhbGci...", "token_type": "bearer"}]
        }
    }


class UserResponse(BaseModel):
    id: int = Field(..., description="ID пользователя в БД")
    email: str = Field(..., description="Email пользователя")

    model_config = {"from_attributes": True}


class RegisterResponse(BaseModel):
    message: str = Field(..., description="Сообщение об успешной регистрации")
    user: UserResponse

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "User registered successfully",
                    "user": {"id": 1, "email": "user@example.com"},
                }
            ]
        }
    }


# ─── Profile ─────────────────────────────────────────────────────────────────

class ProfileResponse(BaseModel):
    email: str = Field(..., description="Email пользователя (используется как имя)")
    courage: int = Field(..., description="Очки смелости")
    completed: int = Field(..., description="Выполненных заданий всего")
    skipped: int = Field(..., description="Пропущенных заданий")
    streak: int = Field(..., description="Дней подряд без пропуска")
    level: str = Field(..., description="Текущий уровень")
    notifications_enabled: bool = Field(..., description="Уведомления включены")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "courage": 34,
                    "completed": 12,
                    "skipped": 1,
                    "streak": 4,
                    "level": "Искатель",
                    "notifications_enabled": False,
                }
            ]
        },
    }


class ProfileUpdateRequest(BaseModel):
    courage: int | None = Field(None, ge=0, description="Новое значение courage")
    completed: int | None = Field(None, ge=0)
    skipped: int | None = Field(None, ge=0)
    streak: int | None = Field(None, ge=0)
    level: str | None = Field(None, max_length=64)
    notifications_enabled: bool | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [{"courage": 44, "streak": 5, "notifications_enabled": True}]
        }
    }


# ─── Challenges ──────────────────────────────────────────────────────────────

ChallengeStatus = Literal["open", "active", "checking", "done", "skipped"]


class ChallengeStateResponse(BaseModel):
    challenge_id: int = Field(..., description="ID задания (1–6 из списка приложения)")
    status: ChallengeStatus = Field(..., description="Статус: open | active | checking | done | skipped")
    photo_url: str | None = Field(None, description="URL фото для photo-type заданий")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{"challenge_id": 3, "status": "done", "photo_url": None}]
        },
    }


class ChallengeStateBulkResponse(BaseModel):
    states: list[ChallengeStateResponse]


class ChallengeStateUpdateRequest(BaseModel):
    status: ChallengeStatus = Field(..., description="Новый статус задания")
    photo_url: str | None = Field(None, description="URL фото (опционально)")

    model_config = {
        "json_schema_extra": {
            "examples": [{"status": "done", "photo_url": None}]
        }
    }
