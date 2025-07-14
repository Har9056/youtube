# backend/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Base
from backend.config import Config

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
