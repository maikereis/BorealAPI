"""
This module is used to hash and unhash password
"""

from logs.customlogger import logger
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password):
    """
    Hashes a password

    Args:
        plain_password (str): a password

    Returns:
        str: a hashed_password
    """
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    """
    Verify if the passed password and the hashed_password found
    in the database matches

    Args:
        plain_password (str): a password
        hashed_password (str): a hashed_password

    Returns:
        bool: True if passwords matches, False if don't.
    """
    logger.info("called")
    passwords_match = pwd_context.verify(plain_password, hashed_password)
    return passwords_match
