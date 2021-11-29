"""
This module defines the object User
"""
import re
from pydantic import BaseModel, validator

RE_EMAILS = "^[a-z][a-z0-9._]+@[a-z0-9]+.([a-z]+).([a-z]+)"


class UserBase(BaseModel):
    """
    A user base has an email as identifier

    Args:
        BaseModel (BaseModel):
        ref: https://pydantic-docs.helpmanual.io/usage/models/
    """

    email: str
    # Verifies if the email matches the format "a.b.c@d.e.f"

    @validator("email")
    def email_has_correct_format(cls, email):
        if re.fullmatch(RE_EMAILS, email):
            return email
        raise ValueError("e-mail invalid")


class UserCreate(UserBase):
    """
    A user needs a password to be created.

    Args:
        UserBase (UserBase):
    """

    password: str

    @validator("password")
    def name_validator(cls, password):
        if isinstance(password, str):
            return password
        raise ValueError("product name invalid")


class User(UserBase):
    """
    A user object

    Args:
        UserBase (UserBase):
    """

    id: int
    is_active: bool

    @validator("id")
    def is_positive(cls, id):
        if id >= 0:
            return id
        raise ValueError("value isn't int")

    @validator("is_active")
    def is_bolean(cls, is_active):
        if isinstance(is_active, bool):
            return is_active
        raise ValueError("value isn't boolean")

    class Config:
        orm_mode = True
