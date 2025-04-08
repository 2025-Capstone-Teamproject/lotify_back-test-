import os
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Lotify"
    API_VERSION: str = "v1"

    # Firebase Admin SDK JSON 파일 경로
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase_admin_key.json")

    # Database URL (예: SQLite 또는 PostgreSQL)
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lotify.db")

    # 기타 보안 관련 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")

settings = Settings()
