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

from app.services.ml_service_ns import predecir_cluster

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
    # Ejecutar predicción con modelo supervisado
    resultado_s = predecir_diabetes(request.dict())
    prediccion = int(resultado_s["prediccion"])
    probabilidad = float(resultado_s["probabilidad"])

    # Ejecutar predicción con modelo no supervisado
    resultado_ns = predecir_cluster(request.dict())

    # Guardar registro en la base de datos (solo resultado supervisado)
    registro = Registro(
        user_id=current_user.id if current_user else None,
        **request.dict(),
        prediccion=prediccion,
        probabilidad=probabilidad
    )
    db.add(registro)
    db.commit()

    # Retornar respuesta combinada usando schema
    return PredictResponse(
        supervisado={"prediccion": prediccion, "probabilidad": probabilidad},
        no_supervisado=resultado_ns
    )



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

