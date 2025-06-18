from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.jwt_handler import create_access_token
from app.core.database import get_db
from app.services.userService import UserService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import requests

router = APIRouter()
user_service = UserService()

@router.post("/auth/kakao/callback", tags=["소셜 로그인"], summary="카카오 소셜 로그인")
async def kakao_callback(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    print(">>> 카카오 콜백 요청 데이터:", data)
    access_token = data.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Missing access_token")

    # 1. 사용자 정보 요청
    profile_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_res = requests.get(profile_url, headers=headers)

    if profile_res.status_code != 200:
        raise HTTPException(status_code=401, detail="Failed to get Kakao user info")

    profile_data = profile_res.json()
    kakao_account = profile_data.get("kakao_account", {})
    nickname = kakao_account.get("profile", {}).get("nickname", "")
    email = kakao_account.get("email") or f"{nickname}@kakao.com"

    if not nickname:
        raise HTTPException(status_code=400, detail="Missing nickname from Kakao")

    # 2. DB 등록 or 로그인 처리
    user = user_service.get_or_create_social_user(
        db=db,
        email=email,
        name=nickname
    )

    # 3. JWT 발급
    jwt_token = create_access_token({"user_id": user.user_id})

    return JSONResponse(
        content=jsonable_encoder({
            "access_token": jwt_token,
            "user_info": {
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "login_type": "kakao"
            }
        }),
        media_type="application/json; charset=utf-8"
    )
