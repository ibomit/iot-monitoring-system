import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise ValueError(
        "SECRET_KEY is not set or shorter than 32 characters"
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
)
REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)
# Send the refresh cookie over HTTPS only. Turn this on in production.
REFRESH_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


def create_access_token(user_id: int) -> str:
    # The JWT spec says "sub" is a string, so the user id is stored as text.
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'sub': str(user_id), 'exp': expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(
    token:str,
) -> dict:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except InvalidTokenError:
        return {}


def generate_refresh_token() -> str:
    # An opaque random string, not a JWT: it is only valid if its hash is in the database.
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    # A fast hash is fine here because the token is long and random, unlike a password.
    return hashlib.sha256(token.encode()).hexdigest()
