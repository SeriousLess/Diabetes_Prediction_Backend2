from pydantic import BaseModel
from datetime import datetime

class RegistroBase(BaseModel):
    RIDAGEYR: int
    RIAGENDR: int
    RIDRETH1: int
    BMXBMI: float
    BMXWAIST: float
    MCQ300C: int
    PAQ605: int
    SMQ020: int
    DMDEDUC2: int
    INDHHIN2: int
    SLD010H: int
    HSD010: int
    prediccion: int
    probabilidad: float

class RegistroResponse(RegistroBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True