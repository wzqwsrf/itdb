# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>



from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from itdblib.models import base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import HSTORE


class AssetInfoModel(base.BASE):

    __tablename__ = 'tb_asset_info'

    asset_id = Column(String(20), primary_key=True)
    asset_type_id = Column(Integer)
    model_id = Column(Integer)
    sn = Column(String(20))
    device_state_id = Column(Integer)
    user_name = Column(String(20))
    store_place_id = Column(Integer)
    store_state_id = Column(Integer)
    up_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    remark = Column(String(100))
    in_out_reason_id = Column(Integer)
    type_info = Column(MutableDict.as_mutable(HSTORE))
