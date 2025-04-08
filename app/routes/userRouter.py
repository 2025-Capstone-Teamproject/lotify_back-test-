from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User
from app.models import schema 
from app.presenters.userPresenter import UserPresenter
from fastapi import Header

router = APIRouter()
presenter = UserPresenter()


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
    
# Authorization: str = Header(...)
@router.post("/social/login", response_model=schema.LoginResponse)
async def firebase_login_user(Authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        return presenter.firebase_login_user(db,Authorization)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")