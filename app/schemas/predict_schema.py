from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    RIDAGEYR: int
    RIAGENDR: int
    BMXBMI: float
    BMXWAIST: float
    MCQ300C: int
    PAQ605: int
    SMQ020: int
    DMDEDUC2: int
    INDHHIN2: int
    SLD010H: int
    HSD010: int

class PredictResponse(BaseModel):
    prediccion: int = Field(..., description="0 = No diabetes, 1 = Riesgo de diabetes")
    probabilidad: float