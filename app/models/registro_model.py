from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 👈 Nuevo

    RIDAGEYR = Column(Integer, nullable=False)
    RIAGENDR = Column(Integer, nullable=False)
    RIDRETH1 = Column(Integer, nullable=False)
    BMXBMI = Column(Float, nullable=False)
    BMXWAIST = Column(Float, nullable=False)
    MCQ300C = Column(Integer, nullable=False)
    PAQ605 = Column(Integer, nullable=False)
    SMQ020 = Column(Integer, nullable=False)
    DMDEDUC2 = Column(Integer, nullable=False)
    INDHHIN2 = Column(Integer, nullable=False)
    SLD010H = Column(Integer, nullable=False)
    HSD010 = Column(Integer, nullable=False)

    prediccion = Column(Integer, nullable=False)
    probabilidad = Column(Float, nullable=False)

    fecha = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con User
    user = relationship("User", back_populates="registros")