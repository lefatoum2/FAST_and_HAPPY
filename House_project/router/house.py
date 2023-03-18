from fastapi import APIRouter, Depends
from House_project.schemas import HouseBase, HouseDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_house
from auth.oauth2 import get_current_user
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
@router.get('/{id}', response_model=HouseDisplay)
def get_house(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_house.get_house(db, id),
        'current_user': current_user
    }
