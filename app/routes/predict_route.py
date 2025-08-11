from fastapi import APIRouter
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.services.ml_service import predecir_diabetes

router = APIRouter(prefix="/prediccion", tags=["Predicción"])

@router.post("/", response_model=PredictResponse)
def obtener_prediccion(request: PredictRequest):
    resultado = predecir_diabetes(request.dict())
    return resultado