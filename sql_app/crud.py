"""
This module defines the interface between the API and the database
"""

from logs.customlogger import logger

from sqlalchemy.orm import Session

from .orm_models import UserOrm

from .models import UserCreate

from .security import hash_password


def get_user_by_email(db: Session, email: str):
    """
    Search a user by email in database.

    Args:
        db (Session): a database session/connection.
        email (str): an email.

    Returns:
        UserOrm: return the user in database.
    """
    logger.info("called")
    return db.query(UserOrm).filter(UserOrm.email == email).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user and register on the database.

    Args:
        db (Session): a database session/connection.
        user (UserCreate): a valid UserCreate with password and email,
        the user's password will be hashed using the SHA256 algorithm,
        before it will be stored.

    Returns:
        UserOrm: return the user in database.
    """
    hashed_password = hash_password(user.password)
    db_user = UserOrm(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
