from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)