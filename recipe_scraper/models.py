from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_books_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Books(DeclarativeBase):
    __tablename__ = "books"

    id = Column(Integer,primary_key = True)
    title = Column('title', String)
    author = Column('author', String, nullable = True)
    genre = Column('genre', String, nullable = True)
    rating = Column('rating', Float, nullable = True)
    no_ratings = Column('no_ratings', String, nullable = True)
    no_reviews = Column('no_reviews', String, nullable = True)
    no_pages = Column('no_pages', String, nullable = True)
    date_publish = Column('date_publish', String, nullable = True)

    
