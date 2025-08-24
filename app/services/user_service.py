from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

def crear_usuario(db: Session, user: UserCreate):
    db_user = User(nombre=user.nombre, correo=user.correo)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user