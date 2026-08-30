from sqlalchemy.orm import Session

from app import models
from app.schemas.user import UserCreate
from app.security import hash_password, verify_password


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
    data: UserCreate
):
    existing_username = get_user_by_username(
        db,
        data.username
    )
    if existing_username is not None: 
        return None, "username_exists"

    existing_email = get_user_by_email(
        db,
        data.email
    )
    if existing_email is not None:
        return None, "email_exists"

    user = models.User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(
            data.password
        )
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user, "created"

    
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