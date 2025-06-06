from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import schema, crud, models
from typing import List
from app.core.jwt_handler import verify_access_token

router = APIRouter()

# 차량 등록
@router.post("/vehicle/register", response_model=schema.getVehicle)
def register_Vehicle(
    vehicle: schema.registerVehicle, 
    db: Session = Depends(get_db),
    user_id: str = depends(verify_access_token),
    ):

    db_vehicle = crud.register_vehicle(db, vehicle, user_id)
    return db_vehicle

# 차량 삭제
@router.delete("/{vehicle_num}", status_code=204)
def delete_Vehicle(vehicle_num: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).get(vehicle_num)
    if not vehicle:
        raise HTTPException(status_code=404, detail="차량을 찾을 수 없습니다.")

    db.delete(vehicle)
    db.commit()
    return Response(status_code=204)

#사용자 차량 조회
@router.get("/{registered_by}", response_model=List[schema.getVehicle])
def show_Vehicles(id: int, db: Session = Depends(get_db)):
    return crud.show_vehicles(db, id)

#장애인 차량 요청 생성
@router.post("/disabled-request", response_model=schema.DisabledRequestResponse)
def create_disabled_vehicle_request(request: schema.DisabledRequest, db: Session = Depends(get_db)):
    return crud.create_disabled_request(db, request)

#장애인 차량 요청 조회
@router.get("/disabled-requests", response_model=List[schema.DisabledRequestResponse])
def list_disabled_requests(db: Session = Depends(get_db)):
    return crud.get_all_pending_requests(db)

#장애인 차량 승인
@router.patch("/disabled-request/{vehicle_num}/{requested_by}/approve", response_model=schema.DisabledRequestResponse)
def approve_disabled_vehicle(vehicle_num: str, requested_by: str, admin_id: str, db: Session = Depends(get_db)):
    return crud.approve_request(db, vehicle_num, requested_by, admin_id)

#장애인 차량 거절
@router.patch("/disabled-request/{vehicle_num}/{requested_by}/reject", response_model=schema.DisabledRequestResponse)
def reject_disabled_vehicle(vehicle_num: str, requested_by: str, admin_id: str, db: Session = Depends(get_db)):
    return crud.reject_request(db, vehicle_num, requested_by, admin_id)
