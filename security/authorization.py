"""
This module is responsible for the authorization process, creating
tokens when a valid user requests one and verifies the received tokens.
"""
from jose import JWTError, JWSError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from security.config import AuthorizationSettings
from logs.customlogger import logger

from exceptions import (
    expired_signature_exception,
    internal_error_exception,
    credentials_exception,
)

from .models import JWTPayload, TokenOwner


auth_settings = AuthorizationSettings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt(sub: str):
    """
    This function creates the JWT, which has a 'sub' and an 'exp'.
    The 'sub' is passed as a parameter, which in this application will
    be the user email.

    The expiration 'exp' will be calculated by the current time that
    token creation was requested plus the lifetime defined by the
    environment variable.(defined in .env file as LIFETIME_MINUTES and
    loaded by auth_settings)

    Args:

        sub (str): the token subject.

    Raises:

        internal_error_exception: if the token can't be created.

    Returns:

        str: return a JWT. A string resulted by hashing the expiration
        date, subject using the secret_key and algorithm
    """
    logger.info("called")

    try:

        # Create the JSON Web Token
        jwt_payload = JWTPayload(
            sub=sub,
            # Perform the expiration time calculation
            exp=datetime.utcnow() + timedelta(minutes=auth_settings.lifetime),
        )

        # Encode the payload
        new_jwt = jwt.encode(
            jwt_payload.dict(),
            auth_settings.secret_key,
            algorithm=auth_settings.algorithm,
        )

        return new_jwt

    except JWSError:
        logger.error("JWT cannot be encoded")
        raise internal_error_exception


async def verify_jwt(jwt_string: str = Depends(oauth2_scheme)):
    """
    This function will:
        1. ensure that the passed token was signed this our API.
        2. the token is not expired.
        3. the token owner is a valid user in database.

    Args:

        jwt_string (str, optional): A JWT passed by request.
        Defaults to Depends(oauth2_scheme).

    Raises:

        credentials_exception: if the token has invalid credentials.

        expired_signature_exception: if the token has expired.

        credentials_exception: if the token can't be decoded.

    Returns:

        TokenOwner: The token owner identification.
    """
    logger.info("called")

    try:
        # Try to decode the JWT content.
        decoded_payload = jwt.decode(
            jwt_string,
            auth_settings.secret_key,
            algorithms=[auth_settings.algorithm],
        )
        # If successfully decoded, reads the content and access the
        # subject with, in this application, must contain the user email.
        email: str = decoded_payload.get("sub")
        if email is None:
            logger.error("Invalid Credentials")
            raise credentials_exception

        jwt_owner = TokenOwner(email=email)
        return jwt_owner

    except jwt.ExpiredSignatureError:
        logger.error("Token Signature Expired")
        raise expired_signature_exception
    # Throw a JWTError when the SECURITY_KEY, ALGORITHM, or anything
    # else goes wrong.
    except JWTError:
        logger.error("Invalid Credentials")
        raise credentials_exception
