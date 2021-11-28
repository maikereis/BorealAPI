from logs.customlogger import logger

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from security.authentication import authenticate_user

from sqlalchemy.orm import Session
from sql_app.database import SessionLocal


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    logger.info("root")
    return {"message": "Hello World"}


@app.post("/")
async def request_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    user = authenticate_user(db_session, form_data.username, form_data.password)
    logger.info(user)
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)
