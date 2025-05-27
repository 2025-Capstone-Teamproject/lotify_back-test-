from typing import Optional
from pydantic import BaseModel
from fastapi import Header

# request
class UserRegister(BaseModel):
    user_id: str
    user_pw: str
    name: str
    email: str
    role: int

class UserLogin(BaseModel):
    user_id: str
    user_pw: str

# firebase 로그인
# class SocialUserLogin(BaseModel):
#     Authorization: str

class RegisterResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    message: str
    access_token: Optional[str] = None

    class Config:
        from_attributes = True
      