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
