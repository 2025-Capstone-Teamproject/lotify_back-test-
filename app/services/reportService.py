from sqlalchemy.orm import Session
from app.schema import reportSchema
from app.models.models import Report

class ReportService:
    async def parking_report(self, db: Session, data: reportSchema.ParkingReport) -> bool:
        try :
            new_report = Report(
                user_id=data.user_id,
                latitude=data.latitude,
                longtitude=data.longtitude,
                file=data.file
            )
            db.add(new_report)
            db.commit()
            print(f"✅ 저장 완료: ID={new_report.id}")
            db.refresh(new_report)
            return True
        except Exception as e:
            print("DB 저장 실패:", e)
            return False