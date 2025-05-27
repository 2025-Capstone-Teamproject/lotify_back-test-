from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from sqlmodel import Field
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

Base.metadata.create_all(engine)