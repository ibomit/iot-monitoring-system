from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.security.dependencies import CurrentUser, AdminUser
from app.dependencies import DbSession
from app.schemas.user import (
    TokenResponse,
    UserCreateRequest,
    UserResponse,
)
from app.security.tokens import (
    REFRESH_COOKIE_SECURE,
    REFRESH_TOKEN_EXPIRE_DAYS,
    create_access_token,
)
from app.services import refresh_token_service, user_service

REFRESH_COOKIE_NAME = "refresh_token"
# The browser only sends the cookie to the auth endpoints, not to every API call.
REFRESH_COOKIE_PATH = "/api/auth"


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


def set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=REFRESH_COOKIE_SECURE,
        samesite="lax",
        path=REFRESH_COOKIE_PATH,
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserCreateRequest,
    db: DbSession,
    admin: AdminUser
):
    return user_service.create_user(
        db,
        data,
    )

@router.post("/login",response_model=TokenResponse)
def login(
    db: DbSession,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = user_service.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    set_refresh_cookie(
        response,
        refresh_token_service.create_refresh_token(db, user.id),
    )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    db: DbSession,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    rotated = None

    if refresh_token is not None:
        rotated = refresh_token_service.rotate_refresh_token(db, refresh_token)

    if rotated is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    user_id, new_refresh_token = rotated
    set_refresh_cookie(response, new_refresh_token)

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    db: DbSession,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if refresh_token is not None:
        refresh_token_service.revoke_refresh_token(db, refresh_token)

    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=REFRESH_COOKIE_SECURE,
        samesite="lax",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_info(
    current_user: CurrentUser,
):
    return current_user
