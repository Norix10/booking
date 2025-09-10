from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,

)
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from .base import Base 
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from 

class User(Base):
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    hashed_password = Column(LargeBinary, nullable=False)
    active = Column(Boolean, default=True)
    