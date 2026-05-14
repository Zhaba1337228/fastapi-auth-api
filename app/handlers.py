"""
Shared business logic used by both v1 and v2 routers.
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, create_user, get_user_by_email, verify_password
from app.schemas import AuthRequest, RegisterResponse, TokenResponse


def handle_register(payload: AuthRequest, db: Session) -> RegisterResponse:
    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    user = create_user(db, payload.email, payload.password)
    from app.schemas import UserResponse
    return RegisterResponse(message="User registered successfully", user=UserResponse.model_validate(user))


def handle_login(payload: AuthRequest, db: Session) -> TokenResponse:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token)
