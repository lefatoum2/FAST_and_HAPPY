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

### Shéma
````python
from pydantic import BaseModel
from typing import List


class House(BaseModel):
    nbstreet: int
    street: str
    postal: str
    city: str

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[House] = []

    class Config():
        orm_mode = True


# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str

    class Config():
        orm_mode = True


class HouseBase(BaseModel):
    nbstreet: int
    street : str
    postal : str
    city : str
    creator_id: int


class HouseDisplay(BaseModel):
    nbstreet: int
    street: str
    postal: str
    city: str
    user: User

    class Config():
        orm_mode = True
````
## Les routers 
house.py

````python
from fastapi import APIRouter, Depends
from House_project.schemas import HouseBase, HouseDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_house
from typing import List
from auth.oauth2 import oauth2_scheme, get_current_user
from House_project.schemas import UserBase

router = APIRouter(
    prefix='/house',
    tags=['house']
)


# Créer une maison
@router.post('/', response_model=HouseDisplay)
def create_house(request: HouseBase, db: Session = Depends(get_db)):
    return db_house.create_house(db, request)


# Avoir une maison
@router.get('/{id}')  # response_model=HouseDisplay)
def get_house(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_house.get_house(db, id),
        'current_user': current_user
    }

````

user.py

````python
from fastapi import APIRouter, Depends
from House_project.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from House_project.db import db_user
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Create User
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Read one user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_user(db, id)


# Update user
@router.post('/{id}/update')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)


# Delete user
@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)

````
## Programme principal
main.py

````python
from fastapi import FastAPI
from router import user
from House_project.router import house
from auth import authentification
from sqlalchemy.engine.base import Engine
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

````

## Gestion de DB
db_house.py

````python
from db.models import DbHouse
from House_project.schemas import HouseBase
from sqlalchemy.orm.session import Session


def create_house(db: Session, request: HouseBase):
    new_house = DbHouse(
        nbstreet=request.nbstreet,
        street=request.street,
        postal=request.postal,
        city=request.city,
        user_id=request.creator_id
    )
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house


def get_house(db: Session, id: int):
    house = db.query(DbHouse).filter(DbHouse.id == id).first()
    return house

````

db_user.py

````python
from sqlalchemy.orm.session import Session
from House_project.schemas import UserBase
from db.models import DbUser
from db.hash import Hash
from fastapi import APIRouter, HTTPException, status


def create_user(db: Session, request: UserBase):
    new_user = DbUser(username=request.username,
                      email=request.email,
                      password=Hash.bcrypt(request.password)
                      )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return
    # return db.query(DbUser).filter(DbUser.id == id).first()


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found")
    return


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)

    })
    db.commit()
    return 'ok'


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return 'ok deleting'

````

hash.py
````python
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes='bcrypt', deprecated='auto')


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)

````
## Token ( authentification)
authentification.py
````python
from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
from db.hash import Hash
from auth import oauth2


router = APIRouter(
    tags=['authentification']
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    access_token = oauth2.create_access_token(data={'sub': user.username})
    return {
        'access_token':access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }

````

oauth2.py
````python
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.param_functions import Depends
from fastapi import APIRouter, HTTPException, status
from db import db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb2ciLCJleHAiOjE2NzkwNTIyMDl9.CvCZfBJL0l1KIuu_TMUq3h7blugYrOtY7lPnLMz1qvo'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authentification": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db_user.get_user_by_username(db, username)

    if user is None:
        raise credentials_exception

    return user

````

NB:
Problème d'autorisation :
house.py
````python
...
# Avoir une maison
@router.get('/{id}')# response_model=HouseDisplay)
def get_house(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data':db_house.get_house(db, id),
        'current_user': current_user
    }
...
````