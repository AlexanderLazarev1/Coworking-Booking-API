

from datetime import timedelta
import app.database as db


def test_login(client):
    resp = client.post("/api/auth/login", json={"login": "Alexandr", "password": "Alex123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    payload = db.decode_token(data["access_token"])
    assert payload["login"] == "Alexandr"
    assert payload["role"] == "admin"


def test_login_wrong_password(client):
    resp = client.post("/api/auth/login", json={"login": "Alexandr", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


def test_login_user_not_found(client):
    resp = client.post("/api/auth/login", json={"login": "unknown", "password": "pass"})
    assert resp.status_code == 401


def test_access_without_token(client):
    resp = client.get("/api/rooms/access", params={"date_res": "2025-12-31"})
    assert resp.status_code == 401


def test_expired_token(client):
    token = db.create_token(data={"login": "Alexandr", "role": "admin"}, expires_delta=timedelta(minutes=-1))
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/rooms/access", params={"date_res": "2025-12-31"}, headers=headers)
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Token expired"