from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.models import utcnow
from app.security.tokens import (
    REFRESH_TOKEN_EXPIRE_DAYS,
    generate_refresh_token,
    hash_refresh_token,
)


def _add_token(db: Session, user_id: int) -> str:
    token = generate_refresh_token()

    db.add(
        models.RefreshToken(
            user_id=user_id,
            token_hash=hash_refresh_token(token),
            expires_at=utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
    )

    return token


def create_refresh_token(db: Session, user_id: int) -> str:
    token = _add_token(db, user_id)
    db.commit()

    return token


def rotate_refresh_token(db: Session, token: str):
    """Swap a valid refresh token for a new one.

    Returns (user_id, new_token), or None if the token is unknown, revoked or
    expired. The old token stops working immediately.
    """
    stored = db.execute(
        select(models.RefreshToken)
        .where(models.RefreshToken.token_hash == hash_refresh_token(token))
        # Lock the row so two simultaneous requests cannot both use the same token.
        .with_for_update()
    ).scalar_one_or_none()

    if stored is None or stored.revoked_at is not None or stored.expires_at <= utcnow():
        return None

    stored.revoked_at = utcnow()
    new_token = _add_token(db, stored.user_id)
    db.commit()

    return stored.user_id, new_token


def revoke_refresh_token(db: Session, token: str) -> None:
    stored = db.execute(
        select(models.RefreshToken)
        .where(models.RefreshToken.token_hash == hash_refresh_token(token))
    ).scalar_one_or_none()

    if stored is not None and stored.revoked_at is None:
        stored.revoked_at = utcnow()
        db.commit()
