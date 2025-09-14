from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,

)
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from App.models.base import Base 

class User(Base):
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    hashed_password = Column(LargeBinary, nullable=False)
    active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    