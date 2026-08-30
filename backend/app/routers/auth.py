from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import CurrentUser
from app.dependencies import DbSession
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.security import create_access_token
from app.services import user_service


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserCreate,
    db: DbSession,
):
    user, result = user_service.create_user(
        db,
        data,
    )

    if result == "username_exists":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if result == "email_exists":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    db: DbSession,
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

    access_token = create_access_token(
        {
            "sub": user.username,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_info(
    current_user: CurrentUser,
):
    return current_user