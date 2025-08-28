from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 👈 Relación opcional con User

    # Variables que sí usamos en el modelo
    RIDAGEYR = Column(Integer, nullable=False)   # Edad
    RIAGENDR = Column(Integer, nullable=False)   # Sexo
    BMXBMI = Column(Float, nullable=False)       # IMC
    BMXWAIST = Column(Float, nullable=False)     # Cintura
    MCQ300C = Column(Integer, nullable=False)    # Historia familiar
    PAQ605 = Column(Integer, nullable=False)     # Actividad física
    SMQ020 = Column(Integer, nullable=False)     # Fumador
    DMDEDUC2 = Column(Integer, nullable=False)   # Educación
    INDHHIN2 = Column(Integer, nullable=False)   # Ingreso
    SLD010H = Column(Integer, nullable=False)    # Horas de sueño
    HSD010 = Column(Integer, nullable=False)     # Salud general

    prediccion = Column(Integer, nullable=False)  # 0 = No diabetes, 1 = Diabetes
    probabilidad = Column(Float, nullable=False)  # Probabilidad del modelo

    fecha = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con User
    user = relationship("User", back_populates="registros")