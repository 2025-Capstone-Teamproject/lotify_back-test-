import os
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Lotify"
    API_VERSION: str = "v1"

    DB_USER: str = os.getenv("USER")
    DB_PASSWORD: str = os.getenv("PASSWD")
    DB_HOST: str = os.getenv("HOST")
    DB_PORT: str = os.getenv("PORT")
    DB_NAME: str = os.getenv("DB")
    
    
    SQLALCHEMY_DATABASE_URL: str = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # 기타 보안 관련 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    
settings = Settings()
