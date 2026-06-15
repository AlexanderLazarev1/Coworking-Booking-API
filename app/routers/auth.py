
import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas import LoginRequest, TokenPayload
from app.database import USERS, create_token, verify_password, decode_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/login")
def login (req: LoginRequest):
    if req.login not in USERS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(req.password, USERS[req.login][2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_token(data={"login": req.login,"role": USERS[req.login][3]})
    return {"access_token": access_token, "token_type": "bearer"}


def current_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> TokenPayload:
    token = creds.credentials
    try:
        payload = decode_token(token)
        login_user = payload.get("login")
        role = payload.get("role")
        if not login_user or not role:
            raise HTTPException(401, "Invalid token payload")
        return TokenPayload(login=login_user, role=role)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")








