from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import SessionLocal, get_db
from app.models.registro_model import Registro
from app.auth.auth_service import get_current_user_optional
from app.models.user_model import User
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.services.ml_service import predecir_diabetes

from app.auth.auth_service import get_current_user
from typing import List

router = APIRouter(prefix="/prediccion", tags=["Predicción"])

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PredictResponse)
def obtener_prediccion(
    request: PredictRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # Ejecutar predicción con ML
    resultado = predecir_diabetes(request.dict())

    # ⚠️ Convertir a tipos nativos de Python para evitar "np.float64"
    prediccion = int(resultado["prediccion"])
    probabilidad = float(resultado["probabilidad"])

    # Guardar registro en la base de datos
    registro = Registro(
        user_id=current_user.id if current_user else None,
        **request.dict(),
        prediccion=prediccion,
        probabilidad=probabilidad
    )
    db.add(registro)
    db.commit()

    # Retornar respuesta
    return PredictResponse(prediccion=prediccion, probabilidad=probabilidad)

@router.get("/historial", response_model=List[dict])
def obtener_historial(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="No autenticado")

    registros = (
        db.query(Registro)
        .filter(Registro.user_id == current_user.id)
        .order_by(Registro.fecha.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "fecha": r.fecha,
            "prediccion": r.prediccion,
            "probabilidad": float(r.probabilidad),  # asegurar JSON-friendly
            
            "RIDAGEYR": r.RIDAGEYR,
            "RIAGENDR": r.RIAGENDR,
            "RIDRETH1": r.RIDRETH1,
            "BMXBMI": r.BMXBMI,
            "BMXWAIST": r.BMXWAIST,
            "MCQ300C": r.MCQ300C,
            "PAQ605": r.PAQ605,
            "SMQ020": r.SMQ020,
            "DMDEDUC2": r.DMDEDUC2,
            "INDHHIN2": r.INDHHIN2,
            "SLD010H": r.SLD010H,
            "HSD010": r.HSD010,
        }
        for r in registros
    ]
    
@router.delete("/{registro_id}")
def eliminar_registro(
    registro_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="No autenticado")

    registro = db.query(Registro).filter(
        Registro.id == registro_id, Registro.user_id == current_user.id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    db.delete(registro)
    db.commit()
    return {"message": "Registro eliminado correctamente"}