# Coworking Booking API

Сервис для бронирования переговорных комнат в коворкинге. Реализована JWT-аутентификация, разделение ролей (администратор / сотрудник), просмотр доступных слотов и полное управление бронированиями.

## Технологии

- Python 3.11
- FastAPI
- JWT (PyJWT)
- Bcrypt (хэширование паролей)
- Pytest (тестирование)
- Docker

## Запуск с помощью Docker (рекомендованный способ)

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/AlexanderLazarev1/Coworking-Booking-API.git
   cd Coworking-Booking-API
   ```

2. **Соберите Docker-образ**

   ```bash
   docker build -t coworking-booking .
   ```

3. **Запустите контейнер**

   ```bash
   docker run -p 8000:8000 coworking-booking
   ```

**После запуска сервис будет доступен по адресу: http://localhost:8000
Интерактивная документация Swagger: http://localhost:8000/docs**

## Локальный запуск (без Docker)

## С использованием Poetry

``` bash
# Установка зависимостей (если есть проблемы с pypi.org, используйте зеркало)
poetry install

#Активация окружения и запуск
poetry run uvicorn app.main:app --reload
```

## С использованием pip

``` bash
# Установка зависимостей
pip install -i https://mirror.yandex.ru/pypi/simple/ fastapi uvicorn[standard] PyJWT bcrypt python-multipart

# Запуск сервера
uvicorn app.main:app --reload
```

## Предустановленные пользователи
| Логин  |	Пароль |  Роль  |
|--------|---------|--------|
|Alexandr|	Alex123| admin  | 
| Sveta  |Sveta123 | empl   |

Примечание - Токен доступа выдаётся на 15 минут. После истечения необходимо выполнить повторный вход.

## Примеры работы с API
Ниже приведены примеры запросов с помощью curl.
Замените <ваш_токен> на реальный JWT-токен, полученный при логине.

1. Аутентификация
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"login": "Alexandr", "password": "Alex123"}'
  ```
Ответ:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
2. Получение списка комнат со слотами на конкретную дату
```bash
curl -X GET "http://localhost:8000/api/rooms/access?date_res=2025-12-31" \
  -H "Authorization: Bearer <ваш_токен>"
```
Пример ответа:

```json
[
  {
    "id_room": 1,
    "name_room": "A",
    "time": "09:00-11:00",
    "slot": 1,
    "is_booked": false,
    "booked_by_me": false
  },
  {
    "id_room": 1,
    "name_room": "A",
    "time": "11:00-13:00",
    "slot": 2,
    "is_booked": true,
    "booked_by_me": false
  }
]
```
3. Создание бронирования
```bash
curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ваш_токен>" \
  -d '{"id_room": 1, "date_booking": "2025-12-31", "slot": 1}'
```
Ответ:

```json
{
  "id": 1,
  "room_id": 1,
  "date": "2025-12-31",
  "slot": 1,
  "created": "2025-01-15T12:34:56.789012+00:00"
}
```
4. Просмотр своих бронирований
```bash
curl -X GET "http://localhost:8000/api/bookings/my" \
  -H "Authorization: Bearer <ваш_токен>"
```
5. Отмена своего бронирования
```bash
curl -X DELETE "http://localhost:8000/api/bookings/1" \
  -H "Authorization: Bearer <ваш_токен>"
```
6. Администратор: просмотр всех бронирований
```bash
curl -X GET "http://localhost:8000/api/admin/allroom" \
  -H "Authorization: Bearer <admin_токен>"
```
7. Администратор: отмена любого бронирования
```bash
curl -X DELETE "http://localhost:8000/api/admin/2" \
  -H "Authorization: Bearer <admin_токен>"
``` 
