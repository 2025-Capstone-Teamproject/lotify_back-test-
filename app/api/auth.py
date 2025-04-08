# from fastapi import APIRouter, Header, HTTPException
# from pydantic import BaseModel, EmailStr
# from app.core.firebase import verify_token
# from app.db.database import SessionLocal
# from app.services.userService import get_or_create_user  # ✅ 경로만 수정됨

# router = APIRouter()
# class LoginResponse(BaseModel):
#     user_id: str
#     email: EmailStr
#     name: str
#     role: int

# @router.post("/login", response_model=LoginResponse)
# def login(Authorization: str = Header(...)):
#     try:
#         id_token = Authorization.split(" ")[1]
#         decoded_token = verify_token(id_token)
#         if not decoded_token:
#             raise HTTPException(status_code=401, detail="Invalid Firebase ID token")

#         firebase_uid = decoded_token["uid"]
#         email = decoded_token.get("email", "")
#         name = decoded_token.get("name", "사용자")

#         db = SessionLocal()
#         user = get_or_create_user(db, uid=firebase_uid, email=email, name=name)

#         return LoginResponse(
#             user_id=user.user_id,
#             email=user.email,
#             name=user.name,
#             role=user.role
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
