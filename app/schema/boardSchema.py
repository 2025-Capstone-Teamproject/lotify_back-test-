from pydantic import BaseModel
from datetime import datetime

#게시글 작성
class writePost(BaseModel):
    title: str
    contents: str


#게시글 조회
class getPost(BaseModel):
    writer: str
    title: str
    contents: str
    view_count: int
    created_at: datetime

    class Config:
        from_attributes = True
