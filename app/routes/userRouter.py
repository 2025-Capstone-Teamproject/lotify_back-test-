from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.models import schema 
from app.presenters.userPresenter import UserPresenter
from fastapi import Header
from app.core.jwt_handler import verify_access_token
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from app.services.userService import UserService

router = APIRouter()
presenter = UserPresenter()
user_service = UserService()

@router.post("/user/register", response_model=schema.RegisterResponse)
async def create_user(user: schema.UserRegister, db: Session = Depends(get_db)):
    try:
        return presenter.register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/user/login", response_model=schema.LoginResponse)
async def login_user(user: schema.UserLogin, db: Session = Depends(get_db)):
    try:
        return presenter.login_user(db,user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    

@router.get("/user/me", tags=["User"], summary="JWT 인증 테스트", description="토큰으로 인증된 사용자만 접근 가능",)
async def get_me(user_id: str = Depends(verify_access_token)):
    return {"message": f"인증된 사용자: {user_id}"}


@router.put("/user/role-update")
def update_user_role(
    user_id: str = Body(...),
    new_role: int = Body(...),
    db: Session = Depends(get_db)
):
    updated = presenter.service.update_user_role(db, user_id, new_role)
    if not updated:
        raise HTTPException(status_code=404, detail="사용자 없음")
    return {"message": f"{user_id}의 역할이 {new_role}으로 변경됨"}


# Authorization: str = Header(...)

# @router.post("/social/login", response_model=schema.LoginResponse)
# async def firebase_login_user(Authorization: str = Header(...), db: Session = Depends(get_db)):
#     try:
#         return presenter.firebase_login_user(db,Authorization)
#     except ValueError as e:
#         raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")