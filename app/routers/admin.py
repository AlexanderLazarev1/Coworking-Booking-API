

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import current_user
from app.schemas import TokenPayload, BookingResponse
from app.database import all_bookings, get_booking_id, delete_booking

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/allroom", response_model=List[BookingResponse])
def get_all_bookings(
        register_user: TokenPayload = Depends(current_user)
):
    if register_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    bookings = all_bookings()
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
    return {"message": "Booking cancelled by admin"}
