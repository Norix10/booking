from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from .base import Base 
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from 

class User(Base):
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    