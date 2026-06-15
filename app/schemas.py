
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class LoginRequest(BaseModel):
    login: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    login: str | None = None
    role: str | None = None


class RoomResponse(BaseModel):
    id_room: int
    name_room: str
    time: str
    slot: int
    is_booked: bool
    booked_by_me: Optional[bool] = False


class BookingRequest(BaseModel):
    id_room: int
    date_booking: date
    slot: int

class BookingResponse(BaseModel):
    id: int
    room_id: int
    date: date
    slot: int
    created: datetime


