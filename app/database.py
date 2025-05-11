from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .core.config import settings

engine = create_engine(url=settings.DATABASE_URL) # the db connection

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # db interaction

Base = declarative_base() # model creation