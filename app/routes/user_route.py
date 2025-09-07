from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import requests
import os

from app.auth import auth_service
from app.auth.auth_schema import UserCreate, UserLogin, Token
from app.models.user_model import User

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

    access_token = auth_service.create_access_token(
        data={"sub": new_user.username}
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

    # 3. Crear token de acceso
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# -------------------
# Perfil protegido
# -------------------
@router.get("/me")
def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return {"username": current_user.username, "email": current_user.email}