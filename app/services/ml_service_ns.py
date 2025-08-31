import joblib
import pandas as pd
from pathlib import Path

# Ignorar warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
###################################################

# Cargar modelos
MODELS_PATH = Path(__file__).resolve().parent.parent / "ml_models"
modelo_ns = joblib.load(MODELS_PATH / "modelo_kmeans.pkl")
scaler_ns = joblib.load(MODELS_PATH / "scaler.pkl")
imputer_ns = joblib.load(MODELS_PATH / "imputer.pkl")
pca_ns = joblib.load(MODELS_PATH / "pca.pkl")

# Columnas esperadas
COLUMNAS = [
    "RIDAGEYR", "RIAGENDR", "BMXBMI", "BMXWAIST",
    "MCQ300C", "PAQ605", "SMQ020", "DMDEDUC2",
    "INDHHIN2", "SLD010H", "HSD010"
]

def predecir_cluster(paciente_dict: dict):
    # Asegurar orden de columnas
    paciente = pd.DataFrame([[paciente_dict[col] for col in COLUMNAS]], columns=COLUMNAS)

    # Preprocesamiento
    paciente_imputado = imputer_ns.transform(paciente)
    paciente_escalado = scaler_ns.transform(paciente_imputado)

    # Predicción de cluster
    cluster = int(modelo_ns.predict(paciente_escalado)[0])

    # Coordenadas PCA (para graficar en frontend)
    coords = pca_ns.transform(paciente_escalado)[0].tolist()

    return {
        "cluster": cluster,
        "pca_coords": {
            "x": float(coords[0]),
            "y": float(coords[1])
        }
    }