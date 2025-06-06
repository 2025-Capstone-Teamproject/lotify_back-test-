from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schema
from datetime import datetime, timedelta

#차량 등록
def register_vehicle(db: Session, vehicle: schema.registerVehicle, registered_by: str):
    db_vehicle = models.Vehicle(
        vehicle_num=vehicle.vehicle_num,
        is_disabled=False,
        registered_by=registered_by
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

#차량 삭제
def delete_vehicle(db: Session, vehicle_num: str):
    vehicle = db.query(models.Vehicle).get(vehicle_num)
    if not vehicle:
        raise HTTPException(status_code=404, detail="차량을 찾을 수 없습니다.")

    db.delete(vehicle)
    db.commit()

#관리자 페이지에서만 보이는 모든 차량 조회 기능
def show_vehicles(db: Session, admin_id: str):
    vehicles = db.query(models.Vehicle).filter(models.Vehicle.registered_by == admin_id).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="등록된 차량이 없습니다.")
    return vehicles

#장애 차량 요청 생성
def create_disabled_request(db: Session, request: schema.DisabledRequest,
requested_by: str = None) -> models.Disabled_Request:
    # requested_by가 제공되지 않은 경우, vehicle의 registered_by 사용
    if not requested_by:
        vehicle = db.query(models.Vehicle).filter(models.Vehicle.vehicle_num == request.vehicle_num).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="차량 정보를 찾을 수 없습니다.")
        requested_by = vehicle.registered_by
    
    # 이미 동일한 vehicle_num과 requested_by로 요청이 존재하는지 확인
    existing_request = db.query(models.Disabled_Request).filter(
        models.Disabled_Request.vehicle_num == request.vehicle_num,
        models.Disabled_Request.requested_by == requested_by
    ).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="이미 해당 차량에 대한 요청이 존재합니다.")
    
    # 새로운 장애인 차량 요청 생성
    db_request = models.Disabled_Request(
        vehicle_num=request.vehicle_num,
        requested_by=requested_by,
        admin_id=request.admin_id,
        status="pending",
        viewed=False,
        approved_at=None
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

#요청 승인
def approve_request(db: Session, vehicle_num: str, requested_by: str, admin_id: str):
    request = db.query(models.Disabled_Request).filter_by(
        vehicle_num=vehicle_num,
        requested_by=requested_by
    ).first()
    if not request or request.status != "pending":
        raise HTTPException(status_code=404, detail="요청을 찾을 수 없거나 이미 처리됨.")

    request.status = "approved"
    request.admin_id = admin_id
    request.approved_at = datetime.utcnow()+timedelta(hours=9)

    # vehicle 테이블 갱신
    vehicle = db.query(models.Vehicle).get(request.vehicle_num)
    if vehicle:
        vehicle.is_disabled = True
        vehicle.approved_by = admin_id
        vehicle.approved_at = datetime.utcnow()+timedelta(hours=9)

    db.commit()
    return request

#요청 거절
def reject_request(db: Session, vehicle_num: str, requested_by: str, admin_id: str):
    request = db.query(models.Disabled_Request).filter_by(
        vehicle_num=vehicle_num,
        requested_by=requested_by
    ).first()

    if not request or request.status != "pending":
        raise HTTPException(status_code=404, detail="요청이 없거나 이미 처리됨.")

    request.status = "rejected"
    request.admin_id = admin_id

    db.commit()
    return request

