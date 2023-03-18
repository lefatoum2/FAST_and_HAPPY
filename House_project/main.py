from fastapi import FastAPI
from router import  user
from House_project.router import house
from auth import authentification
from db.database import engine
from db import models
import uvicorn

app = FastAPI()
app.include_router(authentification.router)
app.include_router(house.router)
app.include_router(user.router)


@app.get('/{name}', tags=['main'])
def index(name: str):
    return f"Hello {name}"


models.Base.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
