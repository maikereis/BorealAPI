"""
This module defines an Object-Relational Mapper
"""

from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class UserOrm(Base):
    """
    A ORM for the API user.

    Args:
        Base (declarative_base):
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
