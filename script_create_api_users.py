from logs.customlogger import logger

from sql_app import crud, orm_models
from sql_app.schemas import UserCreate
from sql_app.database import SessionLocal, engine
from security import authentication

orm_models.Base.metadata.create_all(bind=engine)

users = [
    UserCreate(email="fake_email0@gmail.com", password="pass0"),
    UserCreate(email="fake_email1@gmail.com", password="pass1"),
    UserCreate(email="fake_email2@gmail.com", password="pass2"),
    UserCreate(email="fake_email3@gmail.com", password="pass3"),
]


def create_users(users: list):

    for user in users:
        db_session = SessionLocal()
        if crud.get_user_by_email(db_session, email=user.email):
            logger.info("user already exists.")
        else:
            crud.create_user(db=db_session, user=user)
            logger.info(f"User {user.email}, created!")

    db_session.close()


def get_users(users: list):
    for user in users:
        db_session = SessionLocal()

        try:
            user_in_db = crud.get_user_by_email(db_session, email=user.email)
            if authentication.verify_user_password(
                user.password, user_in_db.hashed_password
            ):
                logger.info("passwords match.")
        except Exception as e:
            logger.exception(e)


create_users(users)
