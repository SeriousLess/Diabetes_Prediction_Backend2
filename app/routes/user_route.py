from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import crear_usuario

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuarios", response_model=UserResponse)
def crear(user: UserCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, user)