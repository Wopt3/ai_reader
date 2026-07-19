#Database
import string

from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.db_url, pool_pre_ping=True, pool_recycle=3600)
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
    path = Column(String)
    audio_path = Column(String)
    time_stamp_path = Column(String)
    title = Column(String)
    pages = Column(Integer)
    user = Column(String)
    last_page = Column(Integer, default=1)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    email = Column(String)
    password = Column(String)
    language = Column(String)


class UserRegister(BaseModel):
    login: str
    password: str
    email:str

class TranslationRequest(BaseModel):
    text: str
    lang: str