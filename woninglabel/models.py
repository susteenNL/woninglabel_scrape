#! -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger, Text, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
from sqlalchemy import event
from sqlalchemy import DDL

DeclarativeBase = declarative_base()

def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """


    # return create_engine('mssql+pyodbc://{0}:{1}@{2}.database.windows.net:1433/{3}?driver=SQL+Server+Native+Client+11.0'.format( settings.DATABASE['db_username'], settings.DATABASE['db_password'], settings.DATABASE['db_host'], settings.DATABASE['db_name'] ), echo=True)
    return create_engine('mssql+pyodbc://{0}:{1}@{2}.database.windows.net:1433/{3}?driver=ODBC+Driver+13+for+SQL+Server'.format( settings.DATABASE['db_username'], settings.DATABASE['db_password'], settings.DATABASE['db_host'], settings.DATABASE['db_name'] ), echo=True)
    # return create_engine( "mssql+pyodbc://{0}".format(settings.DSN) )

def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Categories(DeclarativeBase):

    __tablename__ = "categories"
    
    ID = Column( 'cat_id', Integer, primary_key=True, autoincrement=True )
    Name = Column('cat', String(255), nullable=False)
    ParentID = Column('cat_parent', Integer, nullable=False)
    
    # __table_args__ = ( UniqueConstraint('ItemNumber', name='_item_number'), )
