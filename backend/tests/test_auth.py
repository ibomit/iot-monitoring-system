from datetime import timedelta
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app import models
from app.models import utcnow
from app.schemas.user import UserCreateRequest
from app.security.dependencies import require_admin
from app.security.tokens import hash_refresh_token
from app.services import user_service

USER = {
    "username": "alice",
    "email": "alice@example.com",
    "password": "correct-horse-battery",
}

ADMIN = {
    "username": "boss",
    "email": "boss@example.com",
    "password": "admin-password-123",
}


def register(client, headers=None, **overrides):
    return client.post(
        "/api/auth/register",
        json={**USER, **overrides},
        headers=headers,
    )


def login(client, username=USER["username"], password=USER["password"]):
    return client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )


def auth_headers(client, username, password):
    token = login(client, username, password).json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, db):
    user_service.create_user(db, UserCreateRequest(**ADMIN), role="admin")

    return auth_headers(client, ADMIN["username"], ADMIN["password"])


def test_register_returns_user_without_password(client, admin_headers):
    response = register(client, admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert body["role"] == "user"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_without_token_returns_401(client):
    assert register(client).status_code == 401


def test_register_as_regular_user_returns_403(client, admin_headers):
    register(client, admin_headers)
    user_headers = auth_headers(client, USER["username"], USER["password"])

    response = register(
        client,
        user_headers,
        username="bob",
        email="bob@example.com",
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_register_duplicate_username_returns_409(client, admin_headers):
    register(client, admin_headers)

    response = register(client, admin_headers, email="other@example.com")

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists"


def test_register_duplicate_email_returns_409(client, admin_headers):
    register(client, admin_headers)

    response = register(client, admin_headers, username="bob")

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_register_rejects_short_password(client, admin_headers):
    assert register(client, admin_headers, password="short").status_code == 422


def test_login_and_me(client, admin_headers):
    register(client, admin_headers)

    response = login(client)

    assert response.status_code == 200
    token = response.json()["access_token"]

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me.status_code == 200
    assert me.json()["username"] == "alice"


def test_login_with_wrong_password_returns_401(client, admin_headers):
    register(client, admin_headers)

    response = login(client, password="wrong-password")

    assert response.status_code == 401


def test_login_with_unknown_user_returns_401(client):
    assert login(client, username="nobody").status_code == 401


def test_me_without_token_returns_401(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_with_invalid_token_returns_401(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"})

    assert response.status_code == 401


def test_create_user_defaults_to_user_role_and_accepts_admin(db):
    regular = user_service.create_user(
        db,
        UserCreateRequest(username="regular", email="regular@example.com", password="password123"),
    )
    admin = user_service.create_user(
        db,
        UserCreateRequest(username="boss", email="boss@example.com", password="password123"),
        role="admin",
    )

    assert regular.role == "user"
    assert admin.role == "admin"


def test_require_admin_rejects_non_admin_with_403():
    with pytest.raises(HTTPException) as error:
        require_admin(SimpleNamespace(role="user"))

    assert error.value.status_code == 403


def test_require_admin_allows_admin():
    admin = SimpleNamespace(role="admin")

    assert require_admin(admin) is admin


def refresh(client, token):
    # Sending the Cookie header explicitly replays a specific (e.g. old) token.
    return client.post(
        "/api/auth/refresh",
        headers={"Cookie": f"refresh_token={token}"},
    )


def test_login_sets_httponly_refresh_cookie(client, admin_headers):
    register(client, admin_headers)

    cookie = login(client).headers["set-cookie"].lower()

    assert "refresh_token=" in cookie
    assert "httponly" in cookie
    assert "path=/api/auth" in cookie
    assert "samesite=lax" in cookie


def test_refresh_returns_working_access_token(client, admin_headers):
    register(client, admin_headers)
    token = login(client).cookies["refresh_token"]

    response = refresh(client, token)

    assert response.status_code == 200
    access_token = response.json()["access_token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me.json()["username"] == "alice"


def test_refresh_rotates_the_token(client, admin_headers):
    register(client, admin_headers)
    old_token = login(client).cookies["refresh_token"]

    first = refresh(client, old_token)

    assert first.status_code == 200
    assert first.cookies["refresh_token"] != old_token
    assert refresh(client, old_token).status_code == 401


def test_refresh_without_cookie_returns_401(client):
    assert client.post("/api/auth/refresh").status_code == 401


def test_refresh_with_unknown_token_returns_401(client):
    assert refresh(client, "garbage").status_code == 401


def test_refresh_with_expired_token_returns_401(client, admin_headers, db):
    register(client, admin_headers)
    token = login(client).cookies["refresh_token"]
    stored = (
        db.query(models.RefreshToken)
        .filter(models.RefreshToken.token_hash == hash_refresh_token(token))
        .one()
    )
    stored.expires_at = utcnow() - timedelta(seconds=1)
    db.commit()

    assert refresh(client, token).status_code == 401


def test_logout_revokes_refresh_token(client, admin_headers):
    register(client, admin_headers)
    token = login(client).cookies["refresh_token"]

    response = client.post(
        "/api/auth/logout",
        headers={"Cookie": f"refresh_token={token}"},
    )

    assert response.status_code == 204
    assert refresh(client, token).status_code == 401


def test_logout_without_cookie_returns_204(client):
    assert client.post("/api/auth/logout").status_code == 204
