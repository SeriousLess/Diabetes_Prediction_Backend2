from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.database.connection import Base, engine
from app.models import registro_model
from app.routes import user_route, predict_route

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["https://diabetes-prediction-frontend0.onrender.com"],
    allow_origins=settings.cors_list,  # 👈 ahora usa la lista
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route.router)
app.include_router(predict_route.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Prevención de Diabetes"}