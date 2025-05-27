# app/routes/naverRouter.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import os

from app.core.jwt_handler import create_access_token
from app.core.database import get_db
from app.services.userService import UserService

router = APIRouter()
user_service = UserService()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_REDIRECT_URI = os.getenv("NAVER_REDIRECT_URI")


@router.get("/auth/naver/callback")
def naver_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        raise HTTPException(status_code=400, detail="code or state missing")

    # 1. access_token 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": code,
        "state": state,
    }

    token_res = requests.get(token_url, params=token_params)
    token_data = token_res.json()

    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Failed to get access token")

    # 2. 사용자 정보 요청
    profile_url = "https://openapi.naver.com/v1/nid/me"
    profile_res = requests.get(
        profile_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_data = profile_res.json()

    if profile_data.get("resultcode") != "00":
        raise HTTPException(status_code=400, detail="Failed to fetch user profile")

    user_info = profile_data["response"]
    email = user_info["email"]
    name = user_info.get("name", "")

    # 3. 자동 회원가입 or 로그인
    user = user_service.get_or_create_social_user(
        db=db,
        email=email,
        name=name
    )

    jwt_token = create_access_token({"user_id": user.user_id})
    return {
        "access_token": jwt_token,
        "user_info": {
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "login_type": "naver"
        }
    }
