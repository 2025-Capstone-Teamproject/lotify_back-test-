# app/routes/kakaoRouter.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import os, requests

from app.core.jwt_handler import create_access_token
from app.core.database import get_db
from app.services.userService import UserService

router = APIRouter()
user_service = UserService()

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

@router.get("/auth/kakao/callback")
def kakao_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    # 1. 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code
    }

    token_res = requests.post(token_url, data=token_data)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Failed to get Kakao access token")

    # 2. 사용자 정보 요청
    profile_url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    profile_res = requests.get(profile_url, headers=headers)
    profile_data = profile_res.json()

    kakao_account = profile_data.get("kakao_account", {})
    nickname = kakao_account.get("profile", {}).get("nickname", "")

    if not nickname:
        raise HTTPException(status_code=400, detail="Nickname is required")

    # 이메일 없는 경우 → 임의 생성
    email = kakao_account.get("email") or f"{nickname}@kakao.user"

    # 3. 회원가입 or 로그인
    user = user_service.get_or_create_social_user(
        db=db,
        email=email,
        name=nickname
    )

    jwt_token = create_access_token({"user_id": user.user_id})
    return {
        "access_token": jwt_token,
        "user_info": {
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "login_type": "kakao"
        }
    }
