"""
This module defines the object User
"""
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    A user base has an email as identifier

    Args:
        BaseModel (BaseModel):
        ref: https://pydantic-docs.helpmanual.io/usage/models/
    """

    email: str


class UserCreate(UserBase):
    """
    A user needs a password to be created.

    Args:
        UserBase (UserBase):
    """

    password: str


class User(UserBase):
    """
    A user object

    Args:
        UserBase (UserBase):
    """

    id: int
    is_active: bool

    class Config:
        orm_mode = True
