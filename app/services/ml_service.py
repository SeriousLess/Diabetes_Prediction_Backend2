import joblib
import pandas as pd
from pathlib import Path

# Para ignorar los errores de warning en el terminal
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
###################################################

# Cargar modelos
MODELS_PATH = Path(__file__).resolve().parent.parent / "ml_models"
modelo = joblib.load(MODELS_PATH / "modelo_diabetes.pkl")
scaler = joblib.load(MODELS_PATH / "escalador.pkl")
imputer = joblib.load(MODELS_PATH / "imputador.pkl")

# Columnas esperadas
COLUMNAS = [
    "RIDAGEYR", "RIAGENDR", "BMXBMI", "BMXWAIST",
    "MCQ300C", "PAQ605", "SMQ020", "DMDEDUC2", "INDHHIN2",
    "SLD010H", "HSD010"
]

def predecir_diabetes(paciente_dict: dict):
    # Asegurar orden de columnas
    paciente = pd.DataFrame([[paciente_dict[col] for col in COLUMNAS]], columns=COLUMNAS)

    # Preprocesamiento
    paciente_imputado = imputer.transform(paciente)
    paciente_escalado = scaler.transform(paciente_imputado)

    # Predicción
    prediccion = modelo.predict(paciente_escalado)
    probabilidad = modelo.predict_proba(paciente_escalado)[0][1]

    # ⚠️ Convertir a tipos nativos de Python
    return {
        "prediccion": int(prediccion[0]),
        "probabilidad": float(round(probabilidad, 4))
    }