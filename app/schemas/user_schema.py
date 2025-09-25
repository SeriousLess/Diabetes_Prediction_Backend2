from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
        
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
