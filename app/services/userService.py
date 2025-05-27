from sqlalchemy.orm import Session
from app.models.models import User
from app.models import schema
from passlib.context import CryptContext
# from fastapi import Header

# 비밀번호 해싱 설정 CryptContext : (암호 해시용 컨텍스트 객체)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def create_user(self, db: Session, user_data: schema.UserRegister):
        # 비밀번호 해싱 처리
        hashed_pw = pwd_context.hash(user_data.user_pw)

        new_user = User(
            user_id=user_data.user_id,
            user_pw=hashed_pw,
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_or_create_social_user(self, db: Session, email: str, name: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                user_id=email.split("@")[0],  # ID 없음 → 이메일 기반 임시 ID 생성
                user_pw="",                   # 패스워드 없음
                name=name,
                email=email,
                role=2  # 일반 사용자
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    def update_user_role(self, db: Session, user_id: str, new_role: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
    
    def created_user_id(self, db: Session, user_id: str):
        return db.query(User).filter(User.user_id == user_id).first() is not None
    
    
    def login_user(self, db: Session, user_data: schema.UserLogin):
        user = db.query(User).filter(User.user_id == user_data.user_id).first()
        if not user:
            return "fail: user_id"

        # 해시된 비밀번호 비교
        if not pwd_context.verify(user_data.user_pw, user.user_pw):
            return "fail: user_pw"

        return user
