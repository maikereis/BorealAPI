from logs.customlogger import logger
from sqlalchemy.orm import Session

from sql_app import crud
from sql_app.security import verify_password


def authenticate_user(db: Session, email: str, password: str):
    """
    Start the authentication process:
    1. Search the user in database.
    2. Verify if credentials (password) matches.

        Parameters:
            email : str
                the user identification, in this application is an email.

            password : str
                the user password.

            db : Session
                a database session

    """
    logger.info("called")

    # Search for user in database
    user_in_db = crud.get_user_by_email(db, email=email)

    if not user_in_db:
        logger.info("user not found.")
        return False

    if not verify_password(password, user_in_db.hashed_password):
        return False

    return user_in_db
