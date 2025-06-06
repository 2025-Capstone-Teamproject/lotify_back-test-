from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Double, LargeBinary, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import engine

Base = declarative_base()

# user 테이블
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), unique=True, nullable=False)
    user_pw = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255),nullable=False)
    role = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    adminUser = relationship("AdminUser", uselist=False, back_populates="user")
    report = relationship("Report", uselist=False, back_populates="user")
    
class AdminUser(Base):
    __tablename__ = 'admin_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete=('CASCADE'))) # user 테이블의 id 값을 참조
    region = Column(String(255), nullable=False)
    justification = Column(String(255), nullable=False)
    status = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="adminUser")

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete=('CASCADE')))
    latitude = Column(Double, nullable=False)
    longtitude = Column(Double, nullable=False)
    file = Column(LargeBinary, nullable=False)
    # 신고할때 gps 랑 파일 이미지로 데이터 생성되는데 이부분은 봐야할듯 -> 차 번호는 이미지 추출 ? 사용자가 입력 ? - ? 
    vehicle_num = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="report")
# vehicle_num: 일단 True

# vehicle 테이블
class Vehicle(Base):
    __tablename__ = 'vehicles'

    vehicle_num = Column(String(8), primary_key=True)
    is_disabled = Column(Boolean, default=False, nullable=False)
    registered_by = Column(String(255), ForeignKey("users.user_id"))
    approved_by = Column(String(255), nullable=True)
    approved_at = Column(DateTime(timezone=True))
 
#disabled_request 테이블(장애인 차량 요청 저장)
class Disabled_Request(Base):
    __tablename__ = 'disabled_request'

    vehicle_num = Column(String(8), ForeignKey("vehicles.vehicle_num"), primary_key=True)
    requested_by = Column(String(255), ForeignKey("vehicles.registered_by"), primary_key=True)
    admin_id = Column(String(255), ForeignKey("users.user_id"))
    #요청 상태: pending(대기 중), approved(승인), rejected(거절), 재요청시 다시 pending
    status = Column(String(10), default="pending")
    #조회여부
    viewed = Column(Boolean, default=False)
    approved_at = Column(DateTime(timezone=True), nullable=True)

#게시글 테이블
class Board(Base):
    __tablename__ = 'board'

    num = Column(Integer, primary_key=True, autoincrement=True)
    writer = Column(String(255), ForeignKey("users.user_id"))
    title = Column(String(50), nullable=False)
    contents = Column(Text, nullable=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(engine)