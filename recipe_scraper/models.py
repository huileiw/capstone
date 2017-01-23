from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_recipes_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Recipe(DeclarativeBase):
    __tablename__ = "recipes"

    id = Column(Integer,primary_key = True)
    title = Column('title', String)
    desc = Column('desc', String, nullable = True)
    by = Column('by', String, nullable = True)
    no_made_it = Column('no_made_it', Integer, nullable = True)
    no_reviews = Column('no_reviews', Integer, nullable = True)
    no_ratings = Column('no_ratings', Integer, nullable = True)
    rating = Column('rating', Float, nullable = True)
    servings = Column('servings', Integer, nullable = True)
    prep_time = Column('prep_time', String, nullable = True)
    cook_time = Column('cook_time', String, nullable = True)
    ready_in = Column('ready_in', String, nullable = True)
    no_ingre = Column('no_ingre', Integer, nullable = True)
    no_steps = Column('no_steps', Integer, nullable = True)
    ingre = Column('ingre', String, nullable = True)
    steps = Column('steps', String, nullable = True)
    ntri_cals = Column('ntri_cals', Float, nullable = True)
    ntri_cals_fat  = Column('ntri_cals_fat', Float, nullable = True)
    ntri_tt_fat  = Column('ntri_tt_fat', Float, nullable = True)
    ntri_sat_fat  = Column('ntri_sat_fat', Float, nullable = True)
    ntri_cholstl  = Column('ntri_cholstl', Float, nullable = True)
    ntri_sodium  = Column('ntri_sodium', Float, nullable = True)
    ntri_carbo  = Column('ntri_carbo', Float, nullable = True)
    ntri_sugr  = Column('ntri_sugr', Float, nullable = True)
    ntri_fibr  = Column('ntri_fibr', Float, nullable = True)
    ntri_prtein = Column('ntri_prtein', Float, nullable = True)
    ntri_vA  = Column('ntri_vA', Float, nullable = True)
    ntri_vC = Column('ntri_vC', Float, nullable = True)
    ntri_calc  = Column('ntri_calc', Float, nullable = True)
    ntri_iron  = Column('ntri_iron', Float, nullable = True)
    ntri_potasm = Column('ntri_potasm', Float, nullable = True)
    ntri_thiamin  = Column('ntri_thiamin', Float, nullable = True)
    ntri_niacin  = Column('ntri_niacin', Float, nullable = True)
    ntri_vB6  = Column('ntri_vB6', Float, nullable = True)
    ntri_magnsm  = Column('ntri_magnsm', Float, nullable = True)
    ntri_folate  = Column('ntri_folate', Float, nullable = True)

    
