from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import schemas
from decouple import config

engine = create_engine(config('URL'))


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()



