import re
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, validator
from logs.customlogger import logger
from typing import Optional

RE_EMAILS = "^[a-z][a-z0-9._]+@[a-z0-9]+.([a-z]+).([a-z]+)"


class Token(BaseModel):
    """
    Description

        The class that represents the response when a client request an
        authorization token.

    Attributes

        access_token : str

            the JWT token generated using the client information and
            an expiration date.

        token_type : str

            the token type.
    """
    access_token: str
    token_type: str


class TokenOwner(BaseModel):
    """
    Description

        The class that represents the response when a client request an
        authorization token.

    Attributes

        email : str

            the token owner.
    """
    email: Optional[str] = None

    # Verifies if the email matches the format "a.b.c@d.e.f"
    @validator('email')
    def email_has_correct_format(cls, email):
        if re.fullmatch(RE_EMAILS, email) is None:
            logger.error('invalid e-mail')
            raise ValueError('e-mail invalid')
        return email


class JWTPayload(BaseModel):
    """
    Description

        The class that represents the JSON Web Token payload.

    Attributes

        sub : str

            the subject.

    Methods

        update_exp_date

    """
    sub: str
    exp: Optional[datetime]

    def update_exp_date(self, lifetime: timedelta = timedelta(minutes=15)):
        """
        Update the expiration date by adding the lifetime to the currente
        datetime.

        Paramns:

            lifetime : timedelta

        """
        self.exp = self.datetime.now(timezone.utc) + lifetime

    @validator('sub')
    def email_has_correct_format(cls, sub):
        if re.fullmatch(RE_EMAILS, sub) is None:
            logger.error('sub has an invalid e-mail')
            raise ValueError('e-mail invalid')
        return sub
