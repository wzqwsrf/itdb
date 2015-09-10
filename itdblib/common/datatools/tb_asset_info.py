# -*- coding: utf-8 -*-
#
# author: wangzq <wangzhenqing1008@163.com>
#

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.ext.declarative import *

Base = declarative_base()


class Test(Base):

    __tablename__ = 'tb_asset_info'

    asset_id = Column(String(20), primary_key=True)
    asset_type_id = Column(Integer)
    model_id = Column(Integer)
    sn = Column(String(20))
    mac = Column(String(20))
    device_state_id = Column(Integer)
    user_name = Column(String(20))
    store_place_id = Column(Integer)
    store_state_id = Column(Integer)
    up_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    remark = Column(String(100))
    in_out_reason_id = Column(String(20))
    type_info = Column(MutableDict.as_mutable(HSTORE))


class Crud():

    def __init__(self, session):
        self.session = session

    def getData(self):
        return self.session.query(Test).all()

    def get_data_by_name(self, name):
        return self.session.query(Test).filter(func.lower(Test.name) == func.lower(name)).all()

    def get_data_by_asset_id(self, asset_id):
        return self.session.query(Test).filter(Test.asset_id == asset_id).first()

    def get_data_by_asset_sn(self, sn):
        return self.session.query(Test).filter(func.lower(Test.sn) == func.lower(sn)).first()

    def get_data_asset_id_in_list(self, list):
        return self.session.query(Test).filter(func.upper(Test.asset_id).in_(list)).all()

    def get_all_datas(self):
        return self.session.query(Test).all()


def get_need_data(list):
    # postgresql://hr_user:S@309824650s@l-corehr.ops.beta.cn6:5432/hrcore_v2
    engine = create_engine('postgres://postgres:postgres@localhost/itdb2', echo=False)
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    crud = Crud(session)
    asset_infos = crud.get_data_asset_id_in_list(list)
    print len(asset_infos)
    session.commit()
    return asset_infos


def get_exist_sn_list(params, user_name_equal, user_name_not_equal):
    # postgresql://hr_user:S@309824650s@l-corehr.ops.beta.cn6:5432/hrcore_v2
    engine = create_engine('postgres://postgres:postgres@localhost/itdb2', echo=False)
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    crud = Crud(session)
    asset_infos = []
    for param in params:
        asset_info = crud.get_data_by_asset_sn(param["sn"])
        if asset_info is not None:
            asset_id = asset_info.asset_id.upper()
            if param["sn"] == "CN032K5G6418041J0M5U":
                print 11111111111111
                print asset_id
                print asset_id in user_name_equal
                print asset_id in user_name_not_equal
            if asset_id in user_name_equal or asset_id in user_name_not_equal:
                continue
            if param["sn"] == "CN032K5G6418041J0M5U":
                print u"加入asset——infos"
            asset_infos.append(asset_info.sn.upper())
    print len(asset_infos)
    session.commit()
    return asset_infos

if __name__ == '__main__':
    engine = create_engine('postgres://postgres:postgres@localhost/itdb2', echo=True)
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    crud = Crud(session)
    list = ['a']
    asset_infos = crud.get_data_asset_id_in_list(list)
    print len(asset_infos)
    session.commit()