

from app.schemas import TokenPayload, BookingRequest, BookingResponse
from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import current_user
from app.database import BOOKING, ALL_ROOMS, create_booking, get_booking_id, delete_booking, bookings_user
from app.models import Booking
from datetime import datetime, timezone
from typing import List


router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse)
def book_room(
    req: BookingRequest,
    register_user: TokenPayload = Depends(current_user)):
    if req.date_booking < datetime.now().date():
        raise HTTPException(400, "The date is not relevant")
    if req.id_room not in ALL_ROOMS:
        raise HTTPException(status_code=404, detail="Room not found")
    max_slot = len(ALL_ROOMS[req.id_room]) - 1
    if not (1 <= req.slot <= max_slot):
        raise HTTPException(status_code=400, detail="Incorrect slot number")
    for booking in BOOKING:
        if (booking.room_id == req.id_room and
                booking.date == req.date_booking and
                booking.slot == req.slot):
            raise HTTPException(status_code=409, detail="Slot already booked")
    new_booking = Booking(
        id=None,
        room_id = req.id_room,
        user = register_user.login,
        date_booking = req.date_booking,
        slot = req.slot,
        created = datetime.now(timezone.utc))
    saved_booking = create_booking(new_booking)
    return BookingResponse(
        id = saved_booking.id,
        room_id = saved_booking.room_id,
        date = saved_booking.date,
        slot = saved_booking.slot,
        created = saved_booking.created
    )

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    register_user: TokenPayload = Depends(current_user)
    ):
    booking = get_booking_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if register_user.role != "admin" and register_user.login != booking.user:
        raise HTTPException(status_code=403, detail="Not allowed to cancel this booking")
    delete_booking(booking_id)
    return {"message": "Booking cancelled"}


@router.get("/my", response_model=List[BookingResponse])
def my_bookings(register_user: TokenPayload = Depends(current_user)):
    bookings = bookings_user(register_user.login)
    return [
        BookingResponse(
            id=b.id,
            room_id=b.room_id,
            date=b.date,
            slot=b.slot,
            created=b.created
        )
        for b in bookings
    ]

