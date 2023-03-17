# FastAPI

![img1](https://www.viaggiamo.it/wp-content/uploads/2021/11/fast-and-furious-1-auto.jpg)
## Documentation 
http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

Run : uvicorn main:app1  --reload


## Création de la base de données 
db/database.py
````python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-house.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
````

### Le modèle 
db/models.py
````python
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Date
from sqlalchemy.sql.schema import ForeignKey


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('DbHouse', back_populates='user')


class DbHouse(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True, index=True)
    nbstreet = Column(Integer)
    street = Column(String)
    postal = Column(String)
    city = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DbUser", back_populates='items')

````

## Programme principal
main.py
````python
from fastapi import FastAPI
from router import house_get
from router import house_post
from db import models
from sqlalchemy.engine.base import Engine
from db.database import engine

app = FastAPI()
app.include_router(house_get.router)
app.include_router(house_post.router)


@app.get('/{name}', tags=['main'])
def index(name: str):
    return f"Hello {name}"


models.Base.metadata.create_all(engine)
````