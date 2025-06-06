from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import schema, services, models
from app.schema import vehicleSchema
from typing import List
from app.core.jwt_handler import verify_access_token


router = APIRouter()

# 차량 등록
@router.post("/vehicle/register", response_model=vehicleSchema.getVehicle)
def register_vehicle(
    vehicle: vehicleSchema.registerVehicle, 
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_access_token),
    ):

    db_vehicle = services.register_vehicle(db, vehicle, user_id)
    return db_vehicle

# 차량 삭제
@router.delete("/vehicle/{vehicle_num}", status_code=204)
def delete_vehicle(vehicle_num: str, db: Session = Depends(get_db)):
    services.delete_vehicle(db, vehicle_num)
    return Response(status_code=204)

#사용자 차량 조회
@router.get("/vehicle/{registered_by}", response_model=List[vehicleSchema.getVehicle])
def show_Vehicles(registered_by: int, db: Session = Depends(get_db)):
    return services.show_vehicles(db, id)

#장애인 차량 요청 생성
@router.post("/disabled-request", response_model=vehicleSchema.DisabledRequestResponse)
def create_disabled_vehicle_request(request: vehicleSchema.DisabledRequest, db: Session = Depends(get_db)):
    return services.create_disabled_request(db, request)

#장애인 차량 요청 조회
@router.get("/disabled-requests", response_model=List[vehicleSchema.DisabledRequestResponse])
def list_disabled_requests(db: Session = Depends(get_db)):
    return services.get_all_pending_requests(db)

#장애인 차량 승인
@router.patch("/disabled-request/{vehicle_num}/{requested_by}/approve", response_model=vehicleSchema.DisabledRequestResponse)
def approve_disabled_vehicle(vehicle_num: str, requested_by: str, admin_id: str, db: Session = Depends(get_db)):
    return services.approve_request(db, vehicle_num, requested_by, admin_id)

#장애인 차량 거절
@router.patch("/disabled-request/{vehicle_num}/{requested_by}/reject", response_model=vehicleSchema.DisabledRequestResponse)
def reject_disabled_vehicle(vehicle_num: str, requested_by: str, admin_id: str, db: Session = Depends(get_db)):
    return services.reject_request(db, vehicle_num, requested_by, admin_id)
