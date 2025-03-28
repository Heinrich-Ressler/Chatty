from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .db_base import Base



DATABASE_URL = "sqlite:///./chatty.db"


engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)