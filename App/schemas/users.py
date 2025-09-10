from pydantic import BaseModel, ConfigDict, EmailStr


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
    model_config = ConfigDict(from_attributes=True)

    
class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)