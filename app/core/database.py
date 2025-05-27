from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# DB 연결 엔진
# echo = True 설정이 SQLAlchemy가 실행하는 모든 SQL을 콘솔에 로깅해줌
# 즉 echo = True는 지금 무슨 쿼리 보여주는지 디버깅용
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

# 세션 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 (모든 모델이 상속받음)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()