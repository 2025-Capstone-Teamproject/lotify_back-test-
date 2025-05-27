from google.oauth2 import id_token
from google.auth.transport import requests
import os

from app.core.config import settings

def verify_google_token(token: str):
    try:
        # 구글 토큰 검증
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID  # 클라이언트 ID로 검증
        )

        # 'sub'는 구글에서 발급한 사용자 고유 ID
        user_id = idinfo["sub"]
        email = idinfo["email"]
        name = idinfo.get("name", "")
        picture = idinfo.get("picture", "")

        return {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
        }

    except ValueError:
        return None  # 토큰이 잘못되었거나 만료됨
