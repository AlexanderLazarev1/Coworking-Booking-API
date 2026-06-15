
import copy
import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.database as db
from datetime import timedelta, UTC, datetime

# Сброс перед тестом
@pytest.fixture(autouse=True)
def reset_state():
    original_users = copy.deepcopy(db.USERS)
    original_rooms = copy.deepcopy(db.ALL_ROOMS)
    original_booking_counter = db.booking_id_counter
    db.BOOKING.clear()
    db.booking_id_counter = 1
    db.USERS.clear()
    db.USERS.update(original_users)
    db.ALL_ROOMS.clear()
    db.ALL_ROOMS.update(original_rooms)

    yield

    db.BOOKING.clear()
    db.booking_id_counter = original_booking_counter
    db.USERS.clear()
    db.USERS.update(original_users)
    db.ALL_ROOMS.clear()
    db.ALL_ROOMS.update(original_rooms)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_alex(client):
    resp = client.post("/api/auth/login", json={"login": "Alexandr", "password": "Alex123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_sveta(client):
    resp = client.post("/api/auth/login", json={"login": "Sveta", "password": "Sveta123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def future_date():
    return (datetime.now(UTC).date() + timedelta(days=1)).isoformat()