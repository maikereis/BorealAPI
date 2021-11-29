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
    """
    Create a database session
    """
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
    This function will identify the current user by decoding the token,
    and then verifies if the user is registered on the database.

    Raises:

        credentials_exception: if the user are not in database.

    Returns:

        User: a parsed representation of an user information in database.
    """

    logger.info("called")

    # Search for the user in database, as user
    user = get_user_by_email(db_session, email=token_owner.email)
    if not user:
        raise credentials_exception

    current_user = User.from_orm(user)
    return current_user


def get_breweries():
    """
    Sends a get request to the Breweries API.

    Returns:

        Breweries: an object that holds a Brewery list.
    """
    # Send a request
    breweries_response = requests.get(
        "https://api.openbrewerydb.org/breweries/",
        headers={"Content-Type": "application/json"},
    )

    # Checks if the api response is valid
    if breweries_response.status_code != 200:
        return {"status": "breweries site not found"}

    # Tries to parse the received payload (a list of Breweries)
    # If any brewery in the list has the incorrect format, will
    # raise an exception
    try:
        breweries_list = breweries_response.json()

        # Breweries object will take charge of every validation
        # using the @valitador from pydantic
        return Breweries(all_breweries=breweries_list)
    except Exception as e:
        logger.error(e)
        return {"status": "error, invalid breweries list."}


@app.get("/")
async def root():
    """
        An endpoint just to check if the API is UP!

    Returns:

        Json: just a message.
    """
    logger.info("root")
    return {"message": "Hello World"}


@app.post("/token")
async def request_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    """
    A new JWT will be given to the user that request as long as is
    registered in the database.

    Args:

        form_data (OAuth2PasswordRequestForm, optional): a form data
        received by dependence injection. Defaults to Depends().

        db_session (Session, optional): a database session, needed to
        verify the user credentials. Defaults to Depends(get_db).

    Raises:

        non_user_exception: if the credentials are invalid.

        internal_error_exception: if the token is expired.

    Returns:

        Token: an object that holds a JWT and the token type.
    """
    logger.info("called")

    # OAuth2PasswordRequestForm uses 'username' and 'password' words as
    # default, but in this application i use email and password. The
    # names can't be change but works in the same way.
    user = authenticate_user(db_session,
                             form_data.username,
                             form_data.password)
    if not user:
        raise non_user_exception

    # Try to create a new JWT and pack in a Token object
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
    """
    Receive an Order object, and return the same object. The user in
    session/connection must send a valid JWT.

    Args:

        current_user (User, optional): the user in the session.
        Defaults to Depends(identify_user).

        order (Order, optional): an Order object.
        Defaults to Depends(Order).

    Raises:

        inactive_user_exception: if the found user is marked as
        inactive.

    Returns:

        Order: the same payload received is returned.
    """
    logger.info("called")
    if not current_user.is_active:
        logger.error("Inactive User / Access Denied")
        raise inactive_user_exception
    return order


@app.get("/api/open_breweries")
async def get_breweries(
    current_user: User = Depends(identify_user),
    breweries: Breweries = Depends(get_breweries),
):
    """
    An endpoint that triggers a request for a list of breweries

    Args:

        current_user (User, optional): the user in the session.
        Defaults to Depends(identify_user).

        breweries_list (Breweries, optional): a list of jsons.
        Defaults to Depends(get_breweries).

    Raises:

        inactive_user_exception: if the user is marked as inactive

    Returns:

        Breweries: the Breweries received from Breweries API
    """
    logger.info("called")
    if not current_user.is_active:
        logger.error("Inactive User / Access Denied")
        raise inactive_user_exception

    return breweries


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)
