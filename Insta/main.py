from fastapi import FastAPI
import uvicorn
from db import models
from db.database import engine
from routers import user

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root():
    return "ok"


models.Base.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
