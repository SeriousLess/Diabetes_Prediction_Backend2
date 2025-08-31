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


#class PredictResponse(BaseModel):
#    prediccion: int = Field(..., description="0 = No diabetes, 1 = Riesgo de diabetes")
#    probabilidad: float
    

# Submodelo para el resultado supervisado
class SupervisadoResult(BaseModel):
    prediccion: int = Field(..., description="0 = No diabetes, 1 = Riesgo de diabetes")
    probabilidad: float = Field(..., description="Probabilidad de diabetes")

# Submodelo para el resultado no supervisado
class NoSupervisadoResult(BaseModel):
    cluster: int = Field(..., description="Cluster asignado por el modelo no supervisado")
    pca_coords: dict = Field(..., description="Coordenadas PCA para visualización")

# Modelo de respuesta final
class PredictResponse(BaseModel):
    supervisado: SupervisadoResult
    no_supervisado: NoSupervisadoResult
