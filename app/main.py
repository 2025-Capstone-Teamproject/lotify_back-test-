from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import userRouter, reportRouter
from sqlalchemy import text
from app.routes import googleRouter
from app.routes import naverRouter
from app.routes import kakaoRouter
from app.routes import detectRouter
from app.routes import vehicleRouter
from app.routes import boardRouter
from fastapi.staticfiles import StaticFiles
import os
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware



security = HTTPBearer()

app = FastAPI(
    title="불법 주차 감지 시스템 API",
    tags=["불법 주차 감지 시스템"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swagger에서 Authorization 입력 가능하게 하려면 아래처럼 커스텀 OpenAPI 설정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="불법 주차 감지 시스템 API",
        version="1.0.0",
        description="JWT 토큰 인증 기반 API",
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
app.mount("/frontend", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "frontend")), name="frontend")
app.include_router(userRouter.router)
app.include_router(detectRouter.router)
app.include_router(kakaoRouter.router)
app.include_router(naverRouter.router)
app.include_router(googleRouter.router)
app.include_router(reportRouter.router)
app.include_router(vehicleRouter.router)
app.include_router(boardRouter.router)


@app.get("/")
def root():
    return {"message": "🚗 불법 주차 감지 시스템 서버 작동 중!"}
