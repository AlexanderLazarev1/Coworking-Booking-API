
from typing import List
from fastapi import APIRouter, Depends, Query
from app.routers.auth import current_user
from app.database import ALL_ROOMS, BOOKING
from app.schemas import TokenPayload, RoomResponse
from datetime import date


router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@router.get("/access", response_model=List[RoomResponse])
def get_rooms(
    register_user: TokenPayload = Depends(current_user),
    date_res: date = Query(..., description="Дата YYYY-MM-DD")
):

    result = []
    for room_id, data in ALL_ROOMS.items():
        name = data[0]
        for slot_num, time_slot in enumerate(data[1:], start=1):
            booked = any(
                b.room_id == room_id and b.date == date_res and b.slot == slot_num
                for b in BOOKING
            )
            booked_by_me = any(
                b.room_id == room_id and b.date == date_res and b.slot == slot_num and b.user == register_user.login
                for b in BOOKING
            )
            result.append(RoomResponse(id_room=room_id,
                                   name_room=name,
                                   time=time_slot,
                                   slot=slot_num,
                                   is_booked=booked,
                                   booked_by_me=booked_by_me)
            )
    return result











