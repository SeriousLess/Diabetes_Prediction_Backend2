from sqlalchemy.orm import Session
from app.models.registro_model import Registro
from app.schemas.registro_schema import RegistroBase

def guardar_registro(db: Session, data: RegistroBase):
    nuevo = Registro(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo