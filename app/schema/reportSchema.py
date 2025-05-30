from pydantic import BaseModel
from fastapi import Header

class ParkingReport(BaseModel):
    user_id: str
    latitude: float
    longtitude: float
    file: bytes

# ====== Request Message =======
# 1. user_id token 받아오기
# 2. 위/경도값 받아오기
# 3. 파일 원본 받아오기 -> 원본 파일을 DB에 저장: bytes 형식 -> LargeBinary
# 4. 차 번호는 일단 예외 