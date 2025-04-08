from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = f'mysql+pymysql://{os.environ["USER"]}:{os.environ["PASSWD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/{os.environ["DB"]}?charset=utf8'


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()