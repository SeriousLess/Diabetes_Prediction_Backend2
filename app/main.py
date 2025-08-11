from fastapi import FastAPI
from app.routes import user_route
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine

from app.routes import user_route, predict_route

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todo temporalmente
    #allow_origins=["http://localhost:5173"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Prevención de Diabetes"}

app.include_router(user_route.router)
app.include_router(predict_route.router)