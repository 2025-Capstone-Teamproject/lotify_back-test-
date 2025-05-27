
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.auth.google_auth import verify_google_token
from app.services.userService import UserService
from app.core.jwt_handler import create_access_token
from app.core.database import get_db

router = APIRouter()
user_service = UserService()

class GoogleLoginRequest(BaseModel):
    id_token: str

@router.post("/auth/google-login")
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    user_info = verify_google_token(payload.id_token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Google 토큰 인증 실패")

    user = user_service.get_or_create_social_user(
        db=db,
        email=user_info["email"],
        name=user_info["name"]
    )

    access_token = create_access_token({"user_id": user.user_id})

    return {
        "message": "소셜 로그인 성공",
        "access_token": access_token,
        "user_info": {
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }
