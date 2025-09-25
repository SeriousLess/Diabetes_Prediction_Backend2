from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import requests
import os

from app.auth import auth_service
from app.auth.auth_schema import UserCreate, UserLogin, Token
from app.models.user_model import User

from app.schemas.user_schema import UserUpdate, UserResponse

from app.database.connection import get_db

from app.auth.auth_service import get_current_user


router = APIRouter(prefix="/users", tags=["Usuarios"])

# Clave secreta de reCAPTCHA (ponla en tu .env)
RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET", "TU_SECRET_KEY_AQUI")

# -------------------
# Signup
# -------------------
@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(auth_service.get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed_pw = auth_service.get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 🔹 Ahora el token se crea con el ID del usuario
    access_token = auth_service.create_access_token(
        data={"sub": str(new_user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------
# Login con reCAPTCHA
# -------------------
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(auth_service.get_db)):
    # 1. Validar captcha
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": RECAPTCHA_SECRET, "response": user.token}
    r = requests.post(verify_url, data=payload)
    result = r.json()

    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Captcha inválido ❌")

    # 2. Validar credenciales
    db_user = auth_service.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # 3. Crear token con el ID
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# -------------------
# Perfil protegido
# -------------------
@router.get("/me")
def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}

# -------------------
# Actualizar perfil
# -------------------

@router.put("/me")
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("📩 Datos recibidos:", user_update.dict())

    # Cargar al usuario dentro de esta sesión
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validación de correo
    if user_update.email:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está en uso por otra cuenta"
            )

    # Actualizar
    if user_update.username:
        db_user.username = user_update.username
    if user_update.email:
        db_user.email = user_update.email

    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }