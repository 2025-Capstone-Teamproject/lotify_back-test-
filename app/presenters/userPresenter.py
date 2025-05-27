from sqlalchemy.orm import Session
from app.models import schema
from fastapi import Depends
from app.models.models import User
from app.services.userService import UserService
from app.core.jwt_handler import create_access_token

class UserPresenter:
    def __init__(self):
        self.service = UserService()
    
    def register_user(self, db: Session, user_data: schema.UserRegister):
        if self.service.created_user_id(db, user_data.user_id):
            raise ValueError("이미 존재하는 아이디입니다.")

        self.service.create_user(db, user_data)
        return schema.RegisterResponse(message="회원가입을 축하드립니다.")
    
    def login_user(self, db: Session, user_data: schema.UserLogin):
        login_result = self.service.login_user(db, user_data)
        if login_result == "fail: user_id":
            raise ValueError("아이디를 잘못 입력하셨습니다.")
        
        if login_result == "fail: user_pw":
            raise ValueError("비밀번호를 잘못 입력하셨습니다.")
        
        # 토큰 생성
        access_token = create_access_token({"user_id": login_result.user_id})
        
        # print("✅ access_token:", access_token)
        # print("✅ login_result.user_id:", login_result.user_id)
        # print("✅ return JSON:", {
        #     "message": "로그인에 성공하였습니다.",
        #     "access_token": access_token
        # })
        
        # 결과 값
        return schema.LoginResponse(
            message="로그인에 성공하였습니다.",
            access_token=access_token
        )

    
    # def firebase_login_user(self, db: Session, user_token: schema.SocialUserLogin) -> schema.LoginResponse:
        # login_result = self.service.get_or_create_user(db, user_token)

    #     if login_result == "fail: user_token":
    #         raise ValueError("존재하지 않는 이메일입니다.")

    #     if login_result == "firebase 로그인 성공":
    #         return schema.LoginResponse(message="firebase 로그인 성공")
        
    #     return schema.LoginResponse(message="firbase 계정 회원가입 성공")