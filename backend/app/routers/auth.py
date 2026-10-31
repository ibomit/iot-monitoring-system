from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.security.dependencies import CurrentUser, AdminUser
from app.dependencies import DbSession
from app.schemas.user import (
    TokenResponse,
    UserCreateRequest,
    UserResponse,
)
from app.security.tokens import create_access_token
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

    token = create_access_token(user.id)

    return {
        "access_token": token,
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
