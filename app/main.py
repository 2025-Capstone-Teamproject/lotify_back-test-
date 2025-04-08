# from fastapi import FastAPI
# from routes import userRouter 

# app = FastAPI()

# app.include_router(userRouter.router)

"""
from fastapi import FastAPI
from api import auth

app = FastAPI(title="불법 주차 감지 시스템 API")

# 라우터 등록
app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "🚗 불법 주차 감지 시스템 서버 작동 중!"}
"""

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth
from app.routes import userRouter 

security = HTTPBearer()

app = FastAPI(
    title="불법 주차 감지 시스템 API",
)

# Swagger에서 Authorization 입력 가능하게 하려면 아래처럼 커스텀 OpenAPI 설정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="불법 주차 감지 시스템 API",
        version="1.0.0",
        description="Firebase 토큰 인증 기반 API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 라우터 등록
# app.include_router(auth.router, prefix="/auth")
app.include_router(userRouter.router)

@app.get("/")
def root():
    return {"message": "🚗 불법 주차 감지 시스템 서버 작동 중!"}
