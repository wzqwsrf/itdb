# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from datetime import datetime

from sqlalchemy import Column, String, DateTime
from qg.db.models import HasIdMixin
from itdblib.models import base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import HSTORE


class OperationInfo(base.BASE, HasIdMixin):
    __tablename__ = "tb_operation_info"

    asset_id = Column(String)
    oper_time = Column(DateTime, default=datetime.now)
    oper_type = Column(String)
    operator = Column(String)
    text = Column(String)
    before_field = Column(MutableDict.as_mutable(HSTORE))
    after_field = Column(MutableDict.as_mutable(HSTORE))
