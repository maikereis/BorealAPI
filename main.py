from logs.customlogger import logger

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()


@app.get("/")
async def root():
    logger.info("root")
    return {"message": "Hello World"}


@app.post("/")
async def request_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(form_data)
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)
