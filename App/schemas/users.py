from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    active: bool = True
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password : Optional[str] = None
    
class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)