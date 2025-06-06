from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter(
    tags=["AI 탐지"]
)

# base64 요청용 모델
class ImageBase64Request(BaseModel):
    image_base64: str

@router.post("/detect-file")
async def detect_violation_by_file(file: UploadFile = File(...)):
    """AI 서버로 이미지 파일 업로드하여 불법주차 탐지"""
    try:
        files = {'file': (file.filename, await file.read(), file.content_type)}
        response = requests.post("http://localhost:8001/detect-file", files=files)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect")
async def detect_violation_by_base64(request: ImageBase64Request):
    """AI 서버로 base64 이미지 전송하여 불법주차 탐지"""
    try:
        response = requests.post("http://localhost:8001/detect", json=request.dict())

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))