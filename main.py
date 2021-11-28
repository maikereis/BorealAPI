from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"print": "Hello World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)