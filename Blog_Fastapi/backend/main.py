from fastapi import FastAPI
import uvicorn
import models
from database import engine
import post
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(post.router)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')

# Access right
origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8000, host="127.0.0.1")
