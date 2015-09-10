# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from itdblib.models import base


class AssetConsumeInfoModel(base.BASE):

    __tablename__ = 'tb_asset_consume_info'

    id = Column(Integer, primary_key=True)
    asset_type_id = Column(Integer)
    model_id = Column(Integer)
    user_name = Column(String(20))
    store_place_id = Column(Integer)
    store_state_id = Column(Integer)
    device_state_id = Column(Integer)
    in_num = Column(Integer)
    out_num = Column(Integer)
    in_out_reason_id = Column(Integer)
    up_time = Column(DateTime, default=datetime.now)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    remark = Column(String(100))