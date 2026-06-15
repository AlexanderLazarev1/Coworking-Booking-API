

from datetime import datetime, UTC, timedelta


def test_admin_get_all_bookings(client, auth_alex, auth_sveta, future_date):
    date1 = future_date
    date2 = (datetime.now(UTC).date() + timedelta(days=2)).isoformat()
    client.post("/api/bookings/", json={"id_room": 1, "date_booking": date1, "slot": 1}, headers=auth_sveta)
    client.post("/api/bookings/", json={"id_room": 2, "date_booking": date2, "slot": 2}, headers=auth_alex)
    resp = client.get("/api/admin/allroom", headers=auth_alex)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_admin_all_bookings_forbidden_for_employee(client, auth_sveta):
    resp = client.get("/api/admin/allroom", headers=auth_sveta)
    assert resp.status_code == 403
    assert resp.json()["detail"] == "Admin access required"


def test_admin_all_bookings_no_token(client):
    resp = client.get("/api/admin/allroom")
    assert resp.status_code == 401


def test_admin_all_bookings_empty(client, auth_alex):
    resp = client.get("/api/admin/allroom", headers=auth_alex)
    assert resp.status_code == 200
    assert resp.json() == []

def test_cancel_booking(client, auth_sveta, auth_alex, future_date):
    create = client.post("/api/bookings/", json={"id_room": 1, "date_booking": future_date, "slot": 1},headers=auth_sveta)
    assert create.status_code == 200, create.text
    booking_id = create.json()["id"]
    cancel = client.delete(f"/api/admin/{booking_id}", headers=auth_alex)
    assert cancel.status_code == 200
    # Проверяем, что список пуст
    resp = client.get("/api/admin/allroom", headers=auth_alex)
    assert len(resp.json()) == 0