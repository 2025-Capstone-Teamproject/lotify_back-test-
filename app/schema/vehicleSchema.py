from pydantic import BaseModel
from fastapi import Header
from typing import Optional
from datetime import datetime

#차량 등록
class registerVehicle(BaseModel):
    vehicle_num: str
    is_disabled: bool
    approved_by: str

#차량 조회
class getVehicle(BaseModel):
    vehicle_num: str
    is_disabled: bool
    registered_by: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    class Config:
        orm_mode = True

#장애차량 등록 요청
class DisabledRequest(BaseModel):
    vehicle_num: str
    admin_id: str

#응답 스키마(요청 조회, 승인)
class DisabledRequestResponse(BaseModel):
    vehicle_num: str
    requested_by: str
    status: str
    approved_by: Optional[str]
    approved_at: Optional[datetime]

    class Config:
        orm_mode = True
