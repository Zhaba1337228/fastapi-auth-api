"""
Shared business logic used by both v1 and v2 routers.
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, create_user, get_user_by_email, verify_password
from app.models import ChallengeState, User, UserProfile
from app.schemas import (
    AuthRequest,
    ChallengeStateBulkResponse,
    ChallengeStateResponse,
    ChallengeStateUpdateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)


# ─── Auth ─────────────────────────────────────────────────────────────────────

def handle_register(payload: AuthRequest, db: Session) -> RegisterResponse:
    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    user = create_user(db, payload.email, payload.password)
    # Сразу создаём пустой профиль для нового пользователя
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    db.commit()
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


# ─── Profile ──────────────────────────────────────────────────────────────────

def _get_or_create_profile(user: User, db: Session) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if profile is None:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def handle_get_profile(user: User, db: Session) -> ProfileResponse:
    profile = _get_or_create_profile(user, db)
    return ProfileResponse(
        email=user.email,
        courage=profile.courage,
        completed=profile.completed,
        skipped=profile.skipped,
        streak=profile.streak,
        level=profile.level,
        notifications_enabled=profile.notifications_enabled,
    )


def handle_update_profile(user: User, payload: ProfileUpdateRequest, db: Session) -> ProfileResponse:
    profile = _get_or_create_profile(user, db)
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return ProfileResponse(
        email=user.email,
        courage=profile.courage,
        completed=profile.completed,
        skipped=profile.skipped,
        streak=profile.streak,
        level=profile.level,
        notifications_enabled=profile.notifications_enabled,
    )


# ─── Challenges ───────────────────────────────────────────────────────────────

def handle_get_challenge_states(user: User, db: Session) -> ChallengeStateBulkResponse:
    rows = db.query(ChallengeState).filter(ChallengeState.user_id == user.id).all()
    states = [ChallengeStateResponse.model_validate(r) for r in rows]
    return ChallengeStateBulkResponse(states=states)


def handle_update_challenge_state(
    user: User,
    challenge_id: int,
    payload: ChallengeStateUpdateRequest,
    db: Session,
) -> ChallengeStateResponse:
    row = (
        db.query(ChallengeState)
        .filter(ChallengeState.user_id == user.id, ChallengeState.challenge_id == challenge_id)
        .first()
    )
    if row is None:
        row = ChallengeState(user_id=user.id, challenge_id=challenge_id)
        db.add(row)
    row.status = payload.status
    if payload.photo_url is not None:
        row.photo_url = payload.photo_url
    db.commit()
    db.refresh(row)
    return ChallengeStateResponse.model_validate(row)
