#Database
from lib2to3.pytree import Base

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.db_url(), pool_pre_ping=True, pool_recycle=3600)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try :
        yield db
    finally:
        db.close()
class PDF(Base):
    __tablename__ = "pdf"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    pages = Column(String)
    last_visited = Column(String)
    