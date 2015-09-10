__author__ = 'zhenqingwang'
# -*- encoding:utf-8 -*-

from sqlalchemy.ext.declarative import *
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import HSTORE
from itdblib.models.tb_asset_info import AssetInfoModel
from itdblib.models.dt_in_out_reason import InOutReason
from itdblib.common.time_utils import get_now_date
from sqlalchemy.sql import table, column

import datetime

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

    def add_batch_oper_infos(self, datas):
        print datas
        try:
            engine = create_engine('postgres://postgres:postgres@localhost/itdb', echo=True)
            connection = engine.connect()
            trans = connection.begin()
            # 得到tb_asset_info这个表
            aim = table(
                "tb_operation_info",
                column("asset_id"),
                column("oper_time"),
                column("oper_type"),
                column("operator"),
                column("text"),
                column("before_field"),
                column("after_field"),
            )
            ins = aim.insert()
            connection.execute(ins, datas)
            trans.commit()
        except Exception, _ex:
            msg = "add_batch_oper_infos error: %s" % str(_ex)
            print msg
            return False, msg
        finally:
            connection.close()
        return True, 'add_batch_oper_infos succeed'


if __name__ == '__main__':
    # postgresql://hr_user:S@309824650s@l-corehr.ops.beta.cn6:5432/hrcore_v2
    engine = create_engine('postgres://postgres:postgres@localhost/itdb', echo=True)
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    crud = Crud(session)
    operInfos = []
    for i in range(2):
        operInfo = {}
        operInfo['before_field'] = {}
        # params['after_field']
        after_field = {}
        # after_field[i] = i
        after_field["aa"] = '2'
        after_field["cc"] = '3'
        operInfo['after_field'] = after_field
        operInfo['asset_id'] = 'asset_id'
        operInfo['oper_type'] = '批量入库'
        operInfo['operator'] = 'zhenqing.wang'
        operInfo['text'] = ''
        operInfo['oper_time'] = get_now_date()
        operInfos.append(operInfo)
    crud.add_batch_oper_infos(operInfos)
    session.commit()
