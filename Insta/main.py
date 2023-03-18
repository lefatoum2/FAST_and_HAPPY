from fastapi import FastAPI
import uvicorn
from db import models
from db.database import engine
from routers import user, post
from fastapi.staticfiles import StaticFiles
from auth import authentification


app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentification.router)


@app.get("/")
def root():
    return "ok"


models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
