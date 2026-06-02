from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email_id: EmailStr
    mobile_number: str | None = None
    password: str


class LoginRequest(BaseModel):
    email_id: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email_id: EmailStr
    mobile_number: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }