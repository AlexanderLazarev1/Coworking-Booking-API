
def test_get_rooms_success(client, auth_alex, future_date):
    resp = client.get("/api/rooms/access", params={"date_res": future_date}, headers=auth_alex)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 8  # 2 комнаты * 4 слота


def test_rooms_show_booked_status(client, auth_sveta, future_date):
    # До бронирования
    resp_before = client.get("/api/rooms/access", params={"date_res": future_date}, headers=auth_sveta)
    assert resp_before.status_code == 200
    rooms_before = resp_before.json()
    target = next(r for r in rooms_before if r["id_room"] == 1 and r["slot"] == 1)
    assert target["is_booked"] is False


    # Создаём бронь
    book = client.post("/api/bookings/", json={"id_room": 1, "date_booking": future_date, "slot": 1}, headers=auth_sveta)
    assert book.status_code == 200


    # После бронирования
    resp_after = client.get("/api/rooms/access", params={"date_res": future_date}, headers=auth_sveta)
    assert resp_after.status_code == 200
    rooms_after = resp_after.json()
    target_after = next(r for r in rooms_after if r["id_room"] == 1 and r["slot"] == 1)
    assert target_after["is_booked"] is True
    assert target_after["booked_by_me"] is True