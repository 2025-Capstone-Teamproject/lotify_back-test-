# app/core/db_test.py
from sqlalchemy import text
from app.core.database import engine

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ DB 연결 성공:", result.scalar())
            dbname = conn.execute(text("SELECT DATABASE()")).scalar()
            print("현재 접속된 DB:", dbname)
    except Exception as e:
        print("❌ DB 연결 실패:", str(e))

if __name__ == "__main__":
    test_connection()
