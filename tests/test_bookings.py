
from datetime import datetime, timedelta, UTC


def test_create_booking_success(client, auth_sveta, future_date):
    resp = client.post("/api/bookings/", json={
        "id_room": 1,
        "date_booking": future_date,
        "slot": 1
    }, headers=auth_sveta)
    assert resp.status_code == 200
    data = resp.json()
    assert data["room_id"] == 1
    assert data["slot"] == 1
    assert "id" in data


def test_create_booking_slot_already_taken(client, auth_sveta, auth_alex, future_date):
    data = {"id_room": 1, "date_booking": future_date, "slot": 1}
    # Первое бронирование
    resp1 = client.post("/api/bookings/", json=data, headers=auth_sveta)
    assert resp1.status_code == 200
    # Второе – конфликт
    resp2 = client.post("/api/bookings/", json=data, headers=auth_alex)
    assert resp2.status_code == 409


def test_create_booking_invalid_slot(client, auth_sveta, future_date):
    resp = client.post("/api/bookings/", json={
        "id_room": 1,
        "date_booking": future_date,
        "slot": 5   # не существует
    }, headers=auth_sveta)
    # Сначала проверка даты (она пройдёт), потом слота
    assert resp.status_code == 400
    # В зависимости от порядка проверок в коде
    assert resp.json()["detail"] in ("Incorrect slot number", "The date is not relevant")


def test_create_booking_past_date(client, auth_sveta):
    yesterday = (datetime.now(UTC).date() - timedelta(days=1)).isoformat()
    resp = client.post("/api/bookings/", json={
        "id_room": 1,
        "date_booking": yesterday,
        "slot": 1
    }, headers=auth_sveta)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "The date is not relevant"


def test_my_bookings(client, auth_sveta, future_date):
    # Создаём два бронирования на разные дни
    date1 = future_date
    date2 = (datetime.now(UTC).date() + timedelta(days=2)).isoformat()
    client.post("/api/bookings/", json={"id_room": 1, "date_booking": date1, "slot": 1}, headers=auth_sveta)
    client.post("/api/bookings/", json={"id_room": 2, "date_booking": date2, "slot": 2}, headers=auth_sveta)
    resp = client.get("/api/bookings/my", headers=auth_sveta)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


def test_cancel_own_booking(client, auth_sveta, future_date):
    create = client.post("/api/bookings/", json={"id_room": 1, "date_booking": future_date, "slot": 1}, headers=auth_sveta)
    assert create.status_code == 200, create.text
    booking_id = create.json()["id"]
    cancel = client.delete(f"/api/bookings/{booking_id}", headers=auth_sveta)
    assert cancel.status_code == 200
    # Проверяем, что список пуст
    my = client.get("/api/bookings/my", headers=auth_sveta)
    assert len(my.json()) == 0