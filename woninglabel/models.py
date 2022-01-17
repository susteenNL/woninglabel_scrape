#! -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, BigInteger, Text, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import woninglabel.settings as settings
from sqlalchemy import event
from sqlalchemy import DDL

DeclarativeBase = declarative_base()

def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """


    # return create_engine('mssql+pyodbc://{0}:{1}@{2}:1433/{3}?driver=SQL+Server+Native+Client+11.0'.format( settings.DATABASE['db_username'], settings.DATABASE['db_password'], settings.DATABASE['db_host'], settings.DATABASE['db_name'] ), echo=True)
    return create_engine('mssql+pyodbc://{0}:{1}@{2}:1433/{3}?driver=ODBC+Driver+17+for+SQL+Server'.format( settings.DATABASE['db_username'], settings.DATABASE['db_password'], settings.DATABASE['db_host'], settings.DATABASE['db_name'] ), echo=True)
    # return create_engine('mssql+pyodbc://{0}:{1}@{2}.database.windows.net:1433/{3}?driver=ODBC+Driver+13+for+SQL+Server'.format( settings.DATABASE['db_username'], settings.DATABASE['db_password'], settings.DATABASE['db_host'], settings.DATABASE['db_name'] ), echo=True)
    # return create_engine( "mssql+pyodbc://{0}".format(settings.DSN) )

def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class ItemData(DeclarativeBase):

    __tablename__ = "woninglabel_prijzen"
    
    ID = Column( 'id', Integer, primary_key=True, autoincrement=True )
    ObjectId = Column('object_id', Integer, nullable=True)
    Postcode = Column('postcode', String(6), nullable=True)
    Huisnr = Column('huisnr', Integer, nullable=True)
    Type = Column('type', String(50), nullable=True)
    ScrapeDate = Column('scrape_date', DateTime, nullable=True)
    Bedrijf = Column('bedrijf', String(100), nullable=True)
    Beoordeling = Column('beoordeling', Float, nullable=True)
    BeoordelingAantal = Column('beoordeling_aantal', Integer, nullable=True)
    Levertijd = Column('levertijd', Integer, nullable=True)
    Prijs = Column('prijs', Float, nullable=True)
    
    # __table_args__ = ( UniqueConstraint('ItemNumber', name='_item_number'), )
