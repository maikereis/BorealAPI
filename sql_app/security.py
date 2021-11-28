from logs.customlogger import logger
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password):
    """
    Hash a plain password

    Parameters:
        plain_password: str

    Return:
        hashed_passwrod: str
    """
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    """
    Verify if the passed password and the hashed_password found
    in the database matches

        Parameters:
            plain_password : str
                a unhashed passord.

            hashed_password : str
                a hashed password.

        Returns:
            passwords_match : bool
    """
    logger.info("called")
    passwords_match = pwd_context.verify(plain_password, hashed_password)
    return passwords_match
