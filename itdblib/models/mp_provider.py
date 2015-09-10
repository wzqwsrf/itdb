# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from sqlalchemy import Column, String, Integer
from qg.db.models import HasIdMixin
from itdblib.models import base


class Provider(base.BASE, HasIdMixin):

    __tablename__ = "mp_provider"

    name = Column(String)
    ch_name = Column(String)
    asset_type_id = Column(Integer)
