__author__ = 'zhenqingwang'
# -*- encoding:utf-8 -*-

from sqlalchemy.ext.declarative import *
from sqlalchemy import Column, String
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import HSTORE

Base = declarative_base()


class Student(Base):
    __tablename__ = 'users'

    id = Column(String(20), primary_key=True)
    info = Column(MutableDict.as_mutable(HSTORE))


class Crud():

    def __init__(self, session):
        self.session = session

    def getData(self):
        return self.session.query(Student).all()

    def getDataByKey(self, key):
        return self.session.query

if __name__ == '__main__':
    engine = create_engine('postgres://postgres:postgres@localhost/hstore', echo=True)
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    crud = Crud(session)
    infos = crud.getData()
    print len(infos)
    print infos[0].info
    session.commit()
