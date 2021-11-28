import requests
from logs.customlogger import logger

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from sql_app.models import User
from sql_app.crud import get_user_by_email
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session

from security.models import Token, TokenOwner
from security.authentication import authenticate_user
from security.authorization import create_jwt, verify_jwt

from models import Order, Breweries


from exceptions import (
    non_user_exception,
    internal_error_exception,
    credentials_exception,
    inactive_user_exception,
)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def identify_user(
    token_owner: TokenOwner = Depends(verify_jwt),
    db_session: Session = Depends(get_db)
):
    """
    This function will identify the current session user by decoding the token

    """

    logger.info("called")

    user = get_user_by_email(db_session, email=token_owner.email)
    if not user:
        raise credentials_exception

    current_user = User.from_orm(user)
    return current_user


def get_breweries():
    breweries_response = requests.get(
        "https://api.openbrewerydb.org/breweries/",
        headers={"Content-Type": "application/json"},
    )

    if breweries_response.status_code != 200:
        return {"status": "breweries site not found"}

    try:
        breweries_list = breweries_response.json()
        return Breweries(all_breweries=breweries_list)
    except Exception as e:
        logger.error(e)
        return {"status": "error, breweries list can't be created"}


@app.get("/")
async def root():
    logger.info("root")
    return {"message": "Hello World"}


@app.post("/token")
async def request_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    logger.info("called")

    # OAuth2PasswordRequestForm uses username and password words as default,
    # but in this application i use email and password.
    user = authenticate_user(db_session,
                             form_data.username,
                             form_data.password)
    if not user:
        raise non_user_exception

    try:
        jwt = create_jwt(user.email)
        response_token = Token(access_token=jwt, token_type="Bearer")
        return response_token.dict()
    except Exception as e:
        logger.error(e)
        raise internal_error_exception


@app.post("/api/loop_back")
async def pass_user(current_user: User = Depends(identify_user),
                    order=Depends(Order)):
    if not current_user.is_active:
        logger.error("Inactive User / Access Denied")
        raise inactive_user_exception
    return order


@app.get("/api/open_breweries")
async def get_breweries(
    current_user: User = Depends(identify_user),
    breweries_list: Breweries = Depends(get_breweries),
):
    if not current_user.is_active:
        logger.error("Inactive User / Access Denied")
        raise inactive_user_exception

    return breweries_list


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)
