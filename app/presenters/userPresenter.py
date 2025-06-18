from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.userService import UserService
from app.core.jwt_handler import create_access_token

from app.schema import userSchema
from app.schema import responseSchema

class UserPresenter:
    def __init__(self):
        self.service = UserService()
    
    def register_user(self, db: Session, user_data: userSchema.UserRegister):
        if self.service.created_user_id(db, user_data.user_id):
            raise ValueError("이미 존재하는 아이디입니다.")

        self.service.create_user(db, user_data)
        return userSchema.RegisterResponse(message="회원가입을 축하드립니다.")
    
    def login_user(self, db: Session, user_data: userSchema.UserLogin):
        login_result = self.service.login_user(db, user_data)
        if login_result == "fail: user_id":
            raise ValueError("아이디를 잘못 입력하셨습니다.")
        
        if login_result == "fail: user_pw":
            raise ValueError("비밀번호를 잘못 입력하셨습니다.")
        
        # 토큰 생성
        access_token = create_access_token({"user_id": login_result.user_id})
        user_role = getattr(login_result, "role", None) # 2
        
        # 결과 값 
        return userSchema.LoginResponse(
            message="로그인에 성공하였습니다.",
            access_token=access_token,
            role=user_role # 3
        )

    def admin_request_user(self, db: Session, user_data: userSchema.AdminRequestUser) -> userSchema.MessageResponse:
        request_result = self.service.admin_request_user(db, user_data)
        if request_result == "fail: not user_id":
            raise ValueError("존재하지 않는 아이디입니다.")
        
        return responseSchema.MessageResponse(message="관리자로 승급하셨습니다")
