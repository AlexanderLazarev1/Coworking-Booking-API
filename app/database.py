
import secrets
from datetime import datetime, timedelta, UTC
from typing import List
import jwt
import bcrypt
from app.models import Booking

# Секретный ключ
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Хэширование пароля
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode()

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode())

# Создание JWT-токена
def create_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Декодирование JWT-токена
def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# Данные
USERS = {'Alexandr':[1, 'Alex123', hash_password('Alex123'), 'admin'],
         'Sveta':[2,'Sveta123',hash_password('Sveta123'),'empl'],
         }


ALL_ROOMS = {1:['A', '09:00-11:00', '11:00-13:00', '14:00-16:00', '16:00-18:00'],
         2:['B', '09:00-11:00','11:00-13:00','14:00-16:00','16:00-18:00']
             }


BOOKING = []
booking_id_counter = 1

# Бронирование слота
def create_booking(booking: Booking) -> Booking:
    global booking_id_counter
    booking.id = booking_id_counter
    booking_id_counter += 1
    BOOKING.append(booking)
    return booking

# Проверка бронирования по id
def get_booking_id(booking_id: int):
    for b in BOOKING:
        if b.id == booking_id:
            return b
    return None

# Отмена бронирования
def delete_booking(booking_id: int):
    global BOOKING
    for i, b in enumerate(BOOKING):
        if b.id == booking_id:
            del BOOKING[i]
            return b
    return None

# Определение пользователя
def bookings_user(user: str):
    return [b for b in BOOKING if b.user == user]

# Возвращает список всех бронирований
def all_bookings() -> List[Booking]:
    return BOOKING.copy()

