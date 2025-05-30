from app.services.reportService import ReportService
from sqlalchemy.orm import Session
from app.schema import reportSchema, responseSchema
class ReportPresenter:
    def __init__(self):
        self.service = ReportService()    

    async def parking_report(self, db: Session, data: reportSchema.ParkingReport) -> responseSchema.MessageResponse:
        result = await self.service.parking_report(db, data)
        if not result:
            raise ValueError("잘못된 신고 형식입니다.")
        return responseSchema.MessageResponse(message="신고가 접수되었습니다")

