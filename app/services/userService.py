from sqlalchemy.orm import Session
from app.models.models import User
from app.models import schema
from app.core.firebase import verify_token
# from fastapi import Header

class UserService:
    def create_user(self, db: Session, user_data: schema.UserRegister) -> User:
        new_user = User(
            user_id = user_data.user_id,
            user_pw = user_data.user_pw,
            name = user_data.name,
            email = user_data.email,
            role = user_data.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def created_user_id(self, db: Session, user_id: str) -> bool:
        return db.query(User).filter(User.user_id == user_id).first() is not None
    
    
    def login_user(self, db: Session, user_data: schema.UserLogin) -> str:
        user = db.query(User).filter(User.user_id == user_data.user_id).first()
        if not user:
            return "fail: user_id" 
        
        if user.user_pw != user_data.user_pw:
            return "fail: user_pw"
        
        return { "success" } # 위 두 return 값은 유효성 검증이라 필요. 이 return값은 사용할일X
    

    def get_or_create_user(self,db: Session, user_token: schema.SocialUserLogin) -> str:
        id_token = user_token.split(" ")[1]
        decoded_token = verify_token(id_token)
        print(decoded_token)
        if not decoded_token:
            return "fail: user_token"

        firebase_uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
        name = decoded_token.get("name", "사용자")

        # 기존에 firebase로 회원가입한 전적이 있는 경우
        user = db.query(User).filter(User.email == email).first()
        if user:
            return "firebase 로그인 성공"

        # firebase로 처음 로그인한 경우
        new_user = User(
        user_id=firebase_uid,
        user_pw="",  # Firebase 기반 인증이므로 비밀번호는 빈 문자열
        email=email,
        name=name,
        role=0  # 기본 사용자 권한
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return "firebase 계정 등록 성공"