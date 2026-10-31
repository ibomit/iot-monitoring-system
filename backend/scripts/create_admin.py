"""Create an admin user.

Run from the backend/ folder (so the app package and .env are found):

    uv run python -m scripts.create_admin
"""

import getpass
import sys

from pydantic import ValidationError

from app.database import SessionLocal
from app.exceptions import ConflictError
from app.schemas.user import UserCreateRequest
from app.services import user_service


def main() -> int:
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")

    if password != getpass.getpass("Repeat password: "):
        print("Passwords do not match.")
        return 1

    try:
        data = UserCreateRequest(
            username=username,
            email=email,
            password=password,
        )
    except ValidationError as error:
        for problem in error.errors():
            print(f"{problem['loc'][0]}: {problem['msg']}")
        return 1

    db = SessionLocal()

    try:
        user = user_service.create_user(db, data, role="admin")
        print(f"Created admin '{user.username}' (id {user.id}).")
    except ConflictError as error:
        print(error)
        return 1
    finally:
        db.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
