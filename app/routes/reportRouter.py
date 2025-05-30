from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlalchemy.orm import Session
from typing import Annotated
from app.presenters.reportPresenter import ReportPresenter
from app.schema import reportSchema 
from app.core.database import get_db

router = APIRouter()
presenter = ReportPresenter()

# 파일요청이기에 pydantic 사용 불가
@router.post("/report")
async def parking_report(
    user_id: Annotated[str, Form()],
    latitude: Annotated[float, Form()],
    longtitude: Annotated[float, Form()],
    file: Annotated[UploadFile, Form()],
    db: Session = Depends(get_db)
):
    try:
        file = await file.read()

        report_data = reportSchema.ParkingReport(
            user_id=user_id, 
            latitude=latitude,
            longtitude=longtitude,
            file=file
        )
        return await presenter.parking_report(db,report_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
# ngrok: 무료로 일정시간동안 서버 외부로 배포