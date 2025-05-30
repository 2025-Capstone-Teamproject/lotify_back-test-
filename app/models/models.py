from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Double, LargeBinary, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import engine

Base = declarative_base()

# user 테이블
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), primary_key=True)
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
    vehicle_num = Column(String(255), nullable=True) # 신고할때 gps 랑 파일 이미지로 데이터 생성되는데 이부분은 봐야할듯 -> 차 번호는 이미지 추출 ? 사용자가 입력 ? - ? 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="report")
# vehicle_num: 일단 True
Base.metadata.create_all(engine)