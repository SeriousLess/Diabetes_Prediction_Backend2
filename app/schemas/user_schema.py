from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True