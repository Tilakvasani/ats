from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.database import get_db
from app.models import AuthUser
from app.schemas import SignupRequest, LoginRequest, TokenResponse
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=True)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(user_id: int, email: str) -> str:
    payload = {
        "sub": email,
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


@router.post("/signup", response_model=TokenResponse)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    # Check email already exists
    result = await db.execute(select(AuthUser).where(AuthUser.email_id == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = AuthUser(
        first_name=data.first_name,
        last_name=data.last_name,
        email_id=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return TokenResponse(access_token=create_token(user.user_id, user.email_id))


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AuthUser).where(AuthUser.email_id == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return TokenResponse(access_token=create_token(user.user_id, user.email_id))



async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> AuthUser:
    if credentials is None:
        raise HTTPException(status_code=401,detail="Not authenticated")
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token,settings.jwt_secret_key,algorithms=["HS256"])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401,detail="Invalid token",)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token")

    result = await db.execute(select(AuthUser).where(AuthUser.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401,detail="User not found",)
    return user

@router.get("/me")
async def me(
    current_user: AuthUser = Depends(get_current_user),
):
    return {
        "success": True,
        "message": "User profile fetched successfully",
        "data": {
            "user_id": current_user.user_id,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email_id,
            "is_active": current_user.is_active,
        }
    }