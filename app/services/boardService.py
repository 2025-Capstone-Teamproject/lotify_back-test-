from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schema
from app.models.models import Board
from app.schema import boardSchema


# 게시글 작성
def write_post(db: Session, post_data: boardSchema.writePost, writer: str):
    new_post = models.Board(
        writer=writer,
        title=post_data.title,
        contents=post_data.contents,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 게시글 전체 조회
def get_all_posts(db: Session):
    return db.query(Board).order_by(Board.created_at.desc()).all()

# 게시글 단일 조회
def get_post_by_id(db: Session, post_id: int):
    post = db.query(models.Board).filter(models.Board.num == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")
    post.view_count += 1
    db.commit()
    db.refresh(post)
    return post

# 게시글 삭제
def delete_post(db: Session, post_id: int, user_id: str):
    post = db.query(models.Board).filter(models.Board.num == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")
    if post.writer != user_id:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    db.delete(post)
    db.commit()
