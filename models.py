from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BINARY, create_engine

BASE = declarative_base()
DATABASE_NAME='sqlite:///_sqlite.db'


class ds_model(BASE):
    __tablename__ = 'DS_TABLE'
    id          = Column(Integer,primary_key=True)
    user_id     = Column(Integer,unique = True)
    position    = Column(Integer)
    data        = Column(BINARY(800))

DS_TABLE=ds_model.__table__


#creating tables
DB_ENGINE = create_engine(DATABASE_NAME)
BASE.metadata.create_all(DB_ENGINE)
del DB_ENGINE


#create future engine
from sqlalchemy_aio import ASYNCIO_STRATEGY
DB_ENGINE = create_engine(DATABASE_NAME,strategy=ASYNCIO_STRATEGY)


#clearing namespace
del declarative_base
del ASYNCIO_STRATEGY 
del create_engine
del Column
del Integer
del BINARY
