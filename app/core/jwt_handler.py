from datetime import datetime, timedelta            # 시간 계산을 위한 기본 라이브러리
from jose import JWTError, jwt                      # JWT 인코딩/디코딩 및 예외 처리용
from app.core.config import settings                # .env 설정 불러오기 위한 모듈
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# 보안 키: JWT 서명을 위한 비밀 키 (.env에서 불러옴)
SECRET_KEY = settings.SECRET_KEY
# 사용할 JWT 서명 알고리즘
ALGORITHM = "HS256"
# JWT 토큰 기본 만료 시간 (단위: 분)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# OAuth2PasswordBearer는
# fastapi에 내장된 토큰을 header에서 자동으로 추출해주는 도구
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login") # tokenUrl="/user/login" 이 부분은 문서용

# ✅ JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = None):
    # 원본 데이터 변형 방지를 위해 복사
    to_encode = data.copy() 
    # 만료 시간 설정 (기본: 60분 후)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    # 만료 시간(exp) 필드를 데이터에 추가
    to_encode.update({"exp": expire})
    # JWT 인코딩: 사용자 데이터 + 만료 시간 + 비밀키 + 알고리즘
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # 생성된 JWT 문자열 반환
    return encoded_jwt

# ✅ JWT 토큰 검증 함수
def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        # 토큰 디코딩 및 검증: 서명, 만료 시간 등 확인
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰에 사용자 정보 없음")
        return user_id  # 유효한 경우 payload(dict) 반환
    except JWTError:
        return HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")  # 서명 오류, 만료 등의 문제 발생 시 None 반환
