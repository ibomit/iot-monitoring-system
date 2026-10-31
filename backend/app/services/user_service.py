from sqlalchemy.orm import Session

from app import models
from app.exceptions import ConflictError
from app.schemas.user import UserCreateRequest
from app.security.passwords import hash_password, verify_password


def get_user_by_id(
    db: Session,
    user_id: int,
):
    return db.get(models.User, user_id)

def get_user_by_username(
    db: Session,
    username: str,
):
    return(
        db.query(models.User)
        .filter(
            models.User.username == username
        ).first()
    )

def get_user_by_email(
    db: Session,
    email: str
):
    return(
        db.query(models.User)
        .filter(
            models.User.email == email
        ).first()
    )

def create_user(
    db: Session,
    data: UserCreateRequest,
    role: str = "user",
):
    existing_username = get_user_by_username(
        db,
        data.username
    )
    if existing_username is not None:
        raise ConflictError("Username already exists")

    existing_email = get_user_by_email(
        db,
        data.email
    )
    if existing_email is not None:
        raise ConflictError("Email already exists")

    user = models.User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(
            data.password
        ),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

    
def authenticate_user(
    db: Session,
    username: str,
    password: str,
):
    user = get_user_by_username(
        db,
        username,
    )

    if user is None: 
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None
    
    return user