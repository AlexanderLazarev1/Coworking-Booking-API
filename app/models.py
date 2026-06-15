
from datetime import date, datetime


class Booking:
    def __init__(self, id: int, room_id: int, user: str, date_booking: date, slot: int, created: datetime):
        self.id = id
        self.room_id = room_id
        self.user = user
        self.date = date_booking
        self.slot = slot
        self.created = created

