from sqlalchemy.orm import Session

from .orm_models import UserOrm
from .schemas import UserCreate

from security import authentication


def get_user_by_email(db: Session, email: str):
    """
    Search a user by email in database

    Parameters:
        db : Session
            a database session

        email : str
            the user email

    Return
        bool : True
            if any entry with the email found
        bool : False
            if none entry with  email was found
    """
    return db.query(UserOrm).filter(UserOrm.email == email).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user and register on the database

    Parameters:
        db : Session
            a database session

        user: UserCreate
            a valid UserCreate with password and email, the user's
            password will be hashed using the SHA256 algorithm,
            before it will be stored.

    Return:
        db_user: User

            a User object
    """
    hashed_password = authentication.hash_password(user.password)
    db_user = UserOrm(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
