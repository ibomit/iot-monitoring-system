from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.auth import require_admin

USER = {
    "username": "alice",
    "email": "alice@example.com",
    "password": "correct-horse-battery",
}


def register(client, **overrides):
    return client.post("/api/auth/register", json={**USER, **overrides})


def login(client, username=USER["username"], password=USER["password"]):
    return client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )


def test_register_returns_user_without_password(client):
    response = register(client)

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert body["role"] == "user"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_rejects_short_password(client):
    assert register(client, password="short").status_code == 422


def test_login_and_me(client):
    register(client)

    response = login(client)

    assert response.status_code == 200
    token = response.json()["access_token"]

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me.status_code == 200
    assert me.json()["username"] == "alice"


def test_login_with_wrong_password_returns_401(client):
    register(client)

    response = login(client, password="wrong-password")

    assert response.status_code == 401


def test_login_with_unknown_user_returns_401(client):
    assert login(client, username="nobody").status_code == 401


def test_me_without_token_returns_401(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_with_invalid_token_returns_401(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"})

    assert response.status_code == 401


def test_require_admin_rejects_non_admin_with_403():
    with pytest.raises(HTTPException) as error:
        require_admin(SimpleNamespace(role="user"))

    assert error.value.status_code == 403


def test_require_admin_allows_admin():
    admin = SimpleNamespace(role="admin")

    assert require_admin(admin) is admin
