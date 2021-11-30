"""
This module defines the classes used in the authorization process.
"""

import re
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, validator
from typing import Optional

RE_NAMES = "[A-Za-z]{2,30}"
RE_EMAILS = "^[a-z][a-z0-9._]+@[a-z0-9]+.([a-z]+).([a-z]+)"


class Token(BaseModel):
    """
    The class that represents the response when a client request an
    authorization token.

    Args:

        BaseModel (BaseModel):
        ref: ttps://pydantic-docs.helpmanual.io/usage/models/
    """

    access_token: str
    token_type: str

    @validator("access_token", "token_type")
    def is_string(cls, value):
        if isinstance(value, str):
            return value
        raise ValueError("not a string")

    @validator("token_type")
    def is_token_type_valid(cls, token_type):
        if re.fullmatch(RE_NAMES, token_type):
            return token_type
        raise ValueError("token_type invalid")


class TokenOwner(BaseModel):
    """
    The class that represents the response when a client request an
    authorization token.

    Args:

        BaseModel (BaseModel):
        ref: ttps://pydantic-docs.helpmanual.io/usage/models/

    Raises:

        ValueError: when any validation fails.

    Returns:

        TokenOwner: a representation of the subject in the token.
    """

    email: Optional[str] = None

    # Verifies if the email matches the format "a.b.c@d.e.f"
    @validator("email", allow_reuse=True)
    def email_has_correct_format(cls, email):
        if re.fullmatch(RE_EMAILS, email):
            return email
        raise ValueError("e-mail invalid")


class JWTPayload(BaseModel):
    """
    The class that represents the JSON Web Token payload.

    Args:

        BaseModel (BaseModel):
        ref: ttps://pydantic-docs.helpmanual.io/usage/models/

    Raises:

        ValueError: when any validation fails.

    Returns:

        JWTPayload: a JWT object
    """

    sub: str
    exp: Optional[datetime]

    def update_exp_date(self, lifetime: timedelta = timedelta(minutes=60)):
        """
        Update the expiration date by adding the lifetime to the currente
        datetime.

        Args:

            lifetime (timedelta, optional): the lifetime is used to
            calculate the token expiration date.
            Defaults to timedelta(minutes=15).
        """
        self.exp = self.datetime.now(timezone.utc) + lifetime

    @validator("sub", allow_reuse=True)
    def email_has_correct_format(cls, sub):
        if re.fullmatch(RE_EMAILS, sub):
            return sub
        raise ValueError("e-mail invalid")

    @validator("exp")
    def is_datetime(cls, exp):
        if isinstance(exp, datetime):
            return exp
        raise ValueError("datetime invalid")
