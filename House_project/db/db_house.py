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
