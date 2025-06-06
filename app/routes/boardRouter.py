from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.jwt_handler import verify_access_token
from app import schema, services, models
from app.models.models import Board
from app.services import boardService
from app.schema import boardSchema


router = APIRouter()

# 게시글 작성
@router.post("/post/write", response_model=boardSchema.getPost)
def write_post(
    post_data: boardSchema.writePost,
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_access_token)
):
    return boardService.write_post(db, post_data, user_id)

# 전체 게시글 조회
@router.get("/posts", response_model=List[boardSchema.getPost])
def read_all_posts(db: Session = Depends(get_db)):
    return boardService.get_all_posts(db)

# 특정 게시글 조회 (조회수 증가)
@router.get("/post/{post_id}", response_model=boardSchema.getPost)
def read_single_post(post_id: int, db: Session = Depends(get_db)):
    return boardService.get_post_by_id(db, post_id)

# 게시글 삭제
@router.delete("/post/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_access_token)
):
    boardService.delete_post(db, post_id, user_id)
    return
