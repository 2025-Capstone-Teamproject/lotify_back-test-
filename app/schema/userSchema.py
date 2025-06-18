from typing import Optional
from pydantic import BaseModel
from fastapi import Header

# ====== Request Message =======
class UserRegister(BaseModel):
    user_id: str
    user_pw: str
    name: str
    email: str
    role: int

class UserLogin(BaseModel):
    user_id: str
    user_pw: str

class AdminRequestUser(BaseModel):
    # user_id: str
    justification: str
    region: str

# ====== Response Message =======

class MessageResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True
class RegisterResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    message: str
    access_token: Optional[str] = None
    role: int # 1

    class Config:
        from_attributes = True 
