from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.security import decode_access_token
from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)


def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    payload = decode_access_token(token)

    username = payload.get("sub")

    if username is None:
        raise credentials_exception

    user = user_service.get_user_by_username(
        db,
        username,
    )

    if user is None:
        raise credentials_exception

    return user

CurrentUser = Annotated[
    models.User,
    Depends(get_current_user)
]

def require_admin(
    current_user: CurrentUser,
):
    if current_user.role != "admin": 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            details="Admin access required"
        )
    return current_user


AdminUser = Annotated[
    models.User,
    Depends(require_admin)
]