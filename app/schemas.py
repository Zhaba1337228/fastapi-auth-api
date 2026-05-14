from pydantic import BaseModel, EmailStr, Field, field_validator


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
