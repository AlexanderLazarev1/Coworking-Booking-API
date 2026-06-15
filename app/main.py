
from fastapi import FastAPI
from app.routers import auth, rooms, bookings, admin

app = FastAPI(title="Coworking Booking API")

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {"message": "Coworking Booking Service is running"}

