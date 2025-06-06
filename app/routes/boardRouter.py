from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import schema, crud, models
from typing import List
from app.core.jwt_handler import verify_access_token

router = APIRouter()

@router.post("/post/write", response_model=schema.writePost)
